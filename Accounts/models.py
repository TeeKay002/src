from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField



from django.db import models
from django.contrib.auth.models import User
from django.utils.module_loading import import_string

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Other UserProfile fields here
    phone_number = PhoneNumberField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [('male', 'Male'), ('female', 'Female')]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)

    @property
    def email(self):
        return self.user.email

    @property
    def projects(self):
        # Import Project dynamically to avoid circular dependency
        Project = import_string('project_manager.models.Project')
        # Return projects associated with the user profile
        return Project.objects.filter(user=self.user)


    

# accounts/models.py
from django.contrib.auth.models import Group
from django.db import models

class CustomGroup(Group):
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
