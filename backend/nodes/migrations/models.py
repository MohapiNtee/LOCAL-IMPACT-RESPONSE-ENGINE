"""
Nodes models for LIRE distributed network
"""
from django.db import models
from django.utils import timezone
import uuid


class NetworkNode(models.Model):
    """Distributed network nodes (Gateway, Police, Hospital, etc)"""
    
    NODE_TYPES = [
        ('gateway', 'Gateway Node'),
        ('police', 'Police Node'),
        ('hospital', 'Hospital Node'),
        ('community', 'Community Node'),
        ('backup', 'Backup Node'),
        ('relay', 'Relay Node'),
    ]
    
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('degraded', 'Degraded'),
        ('maintenance', 'Maintenance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    node_type = models.CharField(max_length=50, choices=NODE_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(default=5000)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    capacity = models.IntegerField(default=100)  # Max incidents handled
    current_load = models.IntegerField(default=0)  # Current incidents
    cpu_usage = models.FloatField(default=0.0)
    memory_usage = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_heartbeat = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['status', 'node_type']),
            models.Index(fields=['last_heartbeat']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"
    
    def is_healthy(self):
        """Check if node is healthy"""
        return self.status == 'online' and self.cpu_usage < 80 and self.memory_usage < 80


class NodeConnection(models.Model):
    """Connections between nodes"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name='outgoing_connections'
    )
    target_node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name='incoming_connections'
    )
    is_active = models.BooleanField(default=True)
    latency = models.FloatField(default=0.0)  # in milliseconds
    bandwidth = models.FloatField(default=0.0)  # in Mbps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['source_node', 'target_node']
        ordering = ['-is_active', 'latency']
    
    def __str__(self):
        return f"{self.source_node.name} -> {self.target_node.name}"


class NodeMetric(models.Model):
    """Historical metrics for nodes"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node = models.ForeignKey(NetworkNode, on_delete=models.CASCADE, related_name='metrics')
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    network_io = models.FloatField()  # Mbps
    incidents_processed = models.IntegerField()
    response_time = models.FloatField()  # milliseconds
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['node', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.node.name} - {self.timestamp}"
