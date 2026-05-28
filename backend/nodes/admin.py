"""
Admin configuration for nodes
"""
from django.contrib import admin
from .models import NetworkNode, NodeConnection, NodeMetric


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ['name', 'node_type', 'status', 'current_load', 'cpu_usage', 'last_heartbeat']
    list_filter = ['status', 'node_type', 'last_heartbeat']
    search_fields = ['name', 'location', 'ip_address']
    readonly_fields = ['id', 'created_at', 'last_heartbeat']


@admin.register(NodeConnection)
class NodeConnectionAdmin(admin.ModelAdmin):
    list_display = ['source_node', 'target_node', 'is_active', 'latency']
    list_filter = ['is_active', 'created_at']


@admin.register(NodeMetric)
class NodeMetricAdmin(admin.ModelAdmin):
    list_display = ['node', 'cpu_usage', 'memory_usage', 'timestamp']
    list_filter = ['node', 'timestamp']
