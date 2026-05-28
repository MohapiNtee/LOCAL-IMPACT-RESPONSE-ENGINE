"""
Serializers for responders app
"""
from rest_framework import serializers
from .models import Responder, ResponderShift, ResponderAssignment


class ResponderShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponderShift
        fields = ['id', 'shift_start', 'shift_end', 'is_active', 'created_at']


class ResponderAssignmentSerializer(serializers.ModelSerializer):
    responder_name = serializers.CharField(source='responder.name', read_only=True)
    
    class Meta:
        model = ResponderAssignment
        fields = ['id', 'responder_name', 'incident', 'assigned_at', 'arrived_at', 'completed_at', 'notes']


class ResponderSerializer(serializers.ModelSerializer):
    shifts = ResponderShiftSerializer(many=True, read_only=True)
    assignments = ResponderAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Responder
        fields = [
            'id', 'name', 'responder_type', 'phone', 'email', 'location',
            'latitude', 'longitude', 'status', 'available', 'current_incident',
            'created_at', 'updated_at', 'last_heartbeat', 'shifts', 'assignments'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_heartbeat']


class ResponderCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating responders"""
    
    class Meta:
        model = Responder
        fields = ['name', 'responder_type', 'phone', 'email', 'location', 'latitude', 'longitude']
