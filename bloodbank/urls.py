from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonorAdminViewSet, PatientAdminViewSet

from .views import (
    RegisterView,
    LoginView,
    DonorProfileViewSet,
    PatientProfileViewSet,
     BloodStockViewSet,
   
)

router = DefaultRouter()

# Normal user routes

router.register(r'donor-profile', DonorProfileViewSet, basename='donor-profile')
router.register(r'patient-profile', PatientProfileViewSet, basename="patient-profile")
# Admin routes
router.register(r'admin/donors', DonorAdminViewSet, basename='admin-donors')
router.register(r'admin/patients', PatientAdminViewSet, basename='admin-patients')

# urls.py
router.register(r'blood-stock', BloodStockViewSet, basename="blood-stock")


urlpatterns = [
    # User auth endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # Include all router URLs
    path('', include(router.urls)),
]
