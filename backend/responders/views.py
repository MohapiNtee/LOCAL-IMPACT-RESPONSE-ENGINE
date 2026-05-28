"""
Views for responders app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Responder, ResponderAssignment
from .serializers import ResponderSerializer, ResponderCreateSerializer


class ResponderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing responders
    """
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'responder_type', 'available']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ResponderCreateSerializer
        return ResponderSerializer
    
    @action(detail=True, methods=['post'])
    def assign_to_incident(self, request, pk=None):
        """Assign responder to an incident"""
        responder = self.get_object()
        incident_id = request.data.get('incident_id')
        
        if not incident_id:
            return Response(
                {'error': 'incident_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if responder is available
        if not responder.available:
            return Response(
                {'error': 'Responder is not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create assignment
        assignment = ResponderAssignment.objects.create(
            responder=responder,
            incident_id=incident_id
        )
        
        # Update responder status
        responder.status = 'busy'
        responder.available = False
        responder.save()
        
        return Response(
            {'message': 'Responder assigned successfully'},
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def mark_available(self, request, pk=None):
        """Mark responder as available"""
        responder = self.get_object()
        responder.status = 'available'
        responder.available = True
        responder.current_incident = None
        responder.save()
        
        serializer = self.get_serializer(responder)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available responders"""
        responders = Responder.objects.filter(available=True)
        serializer = self.get_serializer(responders, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get responders grouped by type"""
        responder_type = request.query_params.get('type')
        
        if responder_type:
            responders = Responder.objects.filter(responder_type=responder_type)
        else:
            responders = Responder.objects.all()
        
        serializer = self.get_serializer(responders, many=True)
        return Response(serializer.data)
