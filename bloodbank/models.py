from django.db import models
from django.contrib.auth.models import User
import uuid
# Donor Form submissions

class DonorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="")
    blood_group = models.CharField(max_length=5)
    age = models.IntegerField()
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    quantity = models.PositiveIntegerField()  # quantity to donate
    donation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")  # Pending, Accepted, Rejected

    def __str__(self):
        return f"{self.name} - {self.blood_group}"


class PatientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="")
    blood_group = models.CharField(max_length=10)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)

    hospital_name = models.CharField(max_length=100, default="")
    required_quantity = models.PositiveIntegerField(default=1)  # units of blood
    reason = models.TextField(default="")  # reason for requesting blood

    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")  # Pending, Accepted, Rejected

    def __str__(self):
        return f"{self.name} - {self.blood_group}"
# models.py
class BloodStock(models.Model):
    blood_group = models.CharField(max_length=5, unique=True)
    units = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.blood_group} - {self.units} units"
