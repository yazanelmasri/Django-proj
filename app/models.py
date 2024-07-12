from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    hire_date = models.DateField(default=timezone.now,null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    verified = models.BooleanField(default=False)
    
   
    def __str__(self):
        return self.name

    
