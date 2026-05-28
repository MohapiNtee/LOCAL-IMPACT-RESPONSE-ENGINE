"""
Core utilities and middleware for LIRE
"""
from datetime import datetime
import uuid


def generate_id(prefix="ID"):
    """Generate unique ID with prefix"""
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


def get_current_timestamp():
    """Get current timestamp"""
    return datetime.utcnow().isoformat()


class RequestLoggingMiddleware:
    """Middleware for logging incoming requests"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Log before processing
        print(f"[{get_current_timestamp()}] {request.method} {request.path}")
        
        response = self.get_response(request)
        
        # Log after processing
        print(f"[{get_current_timestamp()}] Response: {response.status_code}")
        return response


class CORSMiddleware:
    """CORS handling middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response
