"""
URLs for responders app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResponderViewSet

router = DefaultRouter()
router.register(r'', ResponderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
