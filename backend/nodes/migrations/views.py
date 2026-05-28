"""
Views for nodes app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import NetworkNode, NodeConnection, NodeMetric
from .serializers import NetworkNodeSerializer, NetworkNodeCreateSerializer, NodeConnectionSerializer, NodeMetricSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing network nodes
    """
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'node_type']
    search_fields = ['name', 'location']
    ordering_fields = ['name', 'created_at', 'current_load']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return NetworkNodeCreateSerializer
        return NetworkNodeSerializer
    
    @action(detail=True, methods=['post'])
    def heartbeat(self, request, pk=None):
        """Update node heartbeat and metrics"""
        node = self.get_object()
        
        # Update heartbeat
        node.last_heartbeat = timezone.now()
        
        # Update metrics if provided
        if 'cpu_usage' in request.data:
            node.cpu_usage = request.data.get('cpu_usage')
        if 'memory_usage' in request.data:
            node.memory_usage = request.data.get('memory_usage')
        if 'current_load' in request.data:
            node.current_load = request.data.get('current_load')
        
        # Update status based on metrics
        if node.cpu_usage > 90 or node.memory_usage > 90:
            node.status = 'degraded'
        elif node.status == 'degraded' and node.cpu_usage < 70 and node.memory_usage < 70:
            node.status = 'online'
        
        node.save()
        
        # Record metric
        NodeMetric.objects.create(
            node=node,
            cpu_usage=node.cpu_usage,
            memory_usage=node.memory_usage,
            network_io=request.data.get('network_io', 0),
            incidents_processed=request.data.get('incidents_processed', 0),
            response_time=request.data.get('response_time', 0)
        )
        
        serializer = self.get_serializer(node)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def healthy_nodes(self, request):
        """Get all healthy nodes"""
        nodes = NetworkNode.objects.filter(status='online')
        healthy = [node for node in nodes if node.is_healthy()]
        serializer = self.get_serializer(healthy, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def network_status(self, request):
        """Get overall network status"""
        total_nodes = NetworkNode.objects.count()
        online_nodes = NetworkNode.objects.filter(status='online').count()
        degraded_nodes = NetworkNode.objects.filter(status='degraded').count()
        offline_nodes = NetworkNode.objects.filter(status='offline').count()
        
        avg_cpu = NetworkNode.objects.values_list('cpu_usage', flat=True)
        avg_cpu_usage = sum(avg_cpu) / len(avg_cpu) if avg_cpu else 0
        
        return Response({
            'total_nodes': total_nodes,
            'online': online_nodes,
            'degraded': degraded_nodes,
            'offline': offline_nodes,
            'average_cpu_usage': avg_cpu_usage
        })
    
    @action(detail=True, methods=['get'])
    def connections(self, request, pk=None):
        """Get node connections"""
        node = self.get_object()
        connections = node.outgoing_connections.all()
        serializer = NodeConnectionSerializer(connections, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def metrics(self, request, pk=None):
        """Get node metrics"""
        node = self.get_object()
        metrics = node.metrics.all()[:100]  # Last 100 metrics
        serializer = NodeMetricSerializer(metrics, many=True)
        return Response(serializer.data)
