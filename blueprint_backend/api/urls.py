from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    ExpeditionViewSet, SamplingLocationViewSet, SampleViewSet,
    TaxonomicAssignmentViewSet, DataExportView, signup, login, logout
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'expeditions', ExpeditionViewSet)
router.register(r'locations', SamplingLocationViewSet)
router.register(r'samples', SampleViewSet)
router.register(r'taxonomy', TaxonomicAssignmentViewSet)

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Authentication
    path('auth/signup/', signup, name='api_signup'),
    path('auth/login/', login, name='api_login'),
    path('auth/logout/', logout, name='api_logout'),
    path('auth/token/', obtain_auth_token, name='api_token_auth'),
    
    # Data export
    path('export/', DataExportView.as_view(), name='data_export'),
    
    # Additional API endpoints will be added here
]
