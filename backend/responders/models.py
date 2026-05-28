"""
Responders models for LIRE
"""
from django.db import models
from django.utils import timezone
import uuid


class Responder(models.Model):
    """First responder model (Police, Hospital, Volunteer, etc)"""
    
    RESPONDER_TYPES = [
        ('police', 'Police'),
        ('hospital', 'Hospital'),
        ('firefighter', 'Firefighter'),
        ('ambulance', 'Ambulance'),
        ('volunteer', 'Volunteer'),
        ('village_leader', 'Village Leader'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
        ('on_leave', 'On Leave'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    responder_type = models.CharField(max_length=50, choices=RESPONDER_TYPES)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    available = models.BooleanField(default=True)
    current_incident = models.ForeignKey(
        'incidents.Incident',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='assigned_responders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_heartbeat = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['status', 'responder_type']),
            models.Index(fields=['available']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_responder_type_display()})"


class ResponderShift(models.Model):
    """Work shifts for responders"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responder = models.ForeignKey(Responder, on_delete=models.CASCADE, related_name='shifts')
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-shift_start']
    
    def __str__(self):
        return f"{self.responder.name} - {self.shift_start}"


class ResponderAssignment(models.Model):
    """Assignment of responders to incidents"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    responder = models.ForeignKey(Responder, on_delete=models.CASCADE, related_name='assignments')
    incident = models.ForeignKey(
        'incidents.Incident',
        on_delete=models.CASCADE,
        related_name='responder_assignments'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    arrived_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-assigned_at']
        unique_together = ['responder', 'incident']
    
    def __str__(self):
        return f"{self.responder.name} -> Incident {self.incident.id}"
