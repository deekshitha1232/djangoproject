from rest_framework import viewsets, generics, permissions, status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import AllowAny

from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import PatientProfile
from .models import DonorProfile
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PatientProfileSerializer,
    DonorProfileSerializer,
    BloodStockSerializer
  
)

# -------------------------------
# Authentication Views
# -------------------------------

# Register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Login
class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        try:
            refresh = RefreshToken.for_user(user)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff
        }, status=status.HTTP_200_OK)

# -------------------------------
# User-level ViewSets
# -------------------------------

class DonorProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DonorProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:  # Admin can see all donors
            return DonorProfile.objects.all()
        return DonorProfile.objects.filter(user=self.request.user)


class PatientProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:  # Admin can see all patients
            return PatientProfile.objects.all()
        return PatientProfile.objects.filter(user=self.request.user)



# class DonorAdminViewSet(viewsets.ModelViewSet):
#     queryset = DonorProfile.objects.all()
#     serializer_class = DonorProfileSerializer
#     permission_classes = [IsAdminUser]  # Only admin access

#     @action(detail=True, methods=["post"])
#     def set_status(self, request, pk=None):
#         donor = self.get_object()
#         status_value = request.data.get("status")
#         if status_value not in ["Pending", "Accepted", "Rejected"]:
#             return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
#         donor.status = status_value
#         donor.save()
#         return Response({"status": donor.status})


# class PatientAdminViewSet(viewsets.ModelViewSet):
#     queryset = PatientProfile.objects.all()
#     serializer_class = PatientProfileSerializer
#     permission_classes = [IsAdminUser]

#     @action(detail=True, methods=["post"])
#     def set_status(self, request, pk=None):
#         patient = self.get_object()
#         status_value = request.data.get("status")
#         if status_value not in ["Pending", "Accepted", "Rejected"]:
#             return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
#         patient.status = status_value
#         patient.save()
#         return Response({"status": patient.status})
# views.py
from .models import BloodStock

class DonorAdminViewSet(viewsets.ModelViewSet):
    queryset = DonorProfile.objects.all()
    serializer_class = DonorProfileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=["post"])
    def set_status(self, request, pk=None):
        donor = self.get_object()
        status_value = request.data.get("status")

        if status_value not in ["Pending", "Accepted", "Rejected"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        # Update stock only if status changes
        if donor.status != status_value:
            if status_value == "Accepted":
                stock, _ = BloodStock.objects.get_or_create(blood_group=donor.blood_group)
                stock.units += donor.quantity
                stock.save()
            elif status_value == "Rejected" and donor.status == "Accepted":
                # Rollback if previously accepted
                stock, _ = BloodStock.objects.get_or_create(blood_group=donor.blood_group)
                stock.units = max(0, stock.units - donor.quantity)
                stock.save()

        donor.status = status_value
        donor.save()
        return Response({"status": donor.status})
class PatientAdminViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=["post"])
    def set_status(self, request, pk=None):
        patient = self.get_object()
        status_value = request.data.get("status")

        if status_value not in ["Pending", "Accepted", "Rejected"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        if patient.status != status_value:
            if status_value == "Accepted":
                stock, _ = BloodStock.objects.get_or_create(blood_group=patient.blood_group)
                if stock.units >= patient.quantity:
                    stock.units -= patient.quantity
                    stock.save()
                else:
                    return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)
            elif status_value == "Rejected" and patient.status == "Accepted":
                # Rollback if previously accepted
                stock, _ = BloodStock.objects.get_or_create(blood_group=patient.blood_group)
                stock.units += patient.quantity
                stock.save()

        patient.status = status_value
        patient.save()
        return Response({"status": patient.status})
# views.py
class BloodStockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BloodStock.objects.all()
    serializer_class = BloodStockSerializer
    permission_classes = [AllowAny]
