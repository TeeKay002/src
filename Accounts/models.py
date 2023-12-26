from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #email = models.EmailField(blank=True, null=True)
    email = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)

    @property
    def email(self):
        return self.user.email
    

# accounts/models.py
from django.contrib.auth.models import Group
from django.db import models

class CustomGroup(Group):
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
