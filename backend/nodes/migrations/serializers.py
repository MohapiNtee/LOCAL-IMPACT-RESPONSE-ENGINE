"""
Serializers for nodes app
"""
from rest_framework import serializers
from .models import NetworkNode, NodeConnection, NodeMetric


class NodeConnectionSerializer(serializers.ModelSerializer):
    source_name = serializers.CharField(source='source_node.name', read_only=True)
    target_name = serializers.CharField(source='target_node.name', read_only=True)
    
    class Meta:
        model = NodeConnection
        fields = ['id', 'source_name', 'target_name', 'is_active', 'latency', 'bandwidth', 'created_at', 'updated_at']


class NodeMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeMetric
        fields = ['id', 'cpu_usage', 'memory_usage', 'network_io', 'incidents_processed', 'response_time', 'timestamp']


class NetworkNodeSerializer(serializers.ModelSerializer):
    connections = NodeConnectionSerializer(source='outgoing_connections', many=True, read_only=True)
    metrics = NodeMetricSerializer(many=True, read_only=True)
    health_status = serializers.SerializerMethodField()
    
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name', 'node_type', 'status', 'ip_address', 'port', 'location',
            'latitude', 'longitude', 'capacity', 'current_load', 'cpu_usage',
            'memory_usage', 'created_at', 'last_heartbeat', 'connections',
            'metrics', 'health_status'
        ]
        read_only_fields = ['id', 'created_at', 'last_heartbeat']
    
    def get_health_status(self, obj):
        return obj.is_healthy()


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating nodes"""
    
    class Meta:
        model = NetworkNode
        fields = ['name', 'node_type', 'ip_address', 'port', 'location', 'latitude', 'longitude', 'capacity']
