from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User, Group
from Accounts.models import CustomGroup, UserProfile
from django.dispatch import receiver
from django.utils import timezone
from guardian.mixins import PermissionRequiredMixin, PermissionListMixin
# Create your models here.
# models.py


class Project(PermissionListMixin, models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50)
    file_upload = models.FileField(upload_to='project_files/', null=True, blank=True)
    need_money = models.BooleanField(default=True)
    amount_needed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    already_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stages = models.TextField(blank=True, null=True, help_text='Enter project stages, separated by commas.')


    def save(self, *args, **kwargs):
        # Call the parent class's save method to ensure the model is saved
        super().save(*args, **kwargs)

        # Create a group with the same name as the project
        group_name = f"{self.name}"
        group, created = CustomGroup.objects.get_or_create(name=group_name)

        try:
            user_profile = UserProfile.objects.get(user=self.user)
            group.creator = user_profile
            group.created_by = user_profile.user  # Assuming created_by is a User field
            group.created_at = timezone.now()
            group.save()
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist for the user
            # You might want to create a UserProfile instance here or handle it based on your requirements
            pass

@receiver(post_save, sender=Project)
def create_project_group(sender, instance, created, **kwargs):
    if created:
        group_name = f"{instance.name}"
        group, created = CustomGroup.objects.get_or_create(name=group_name)

        try:
            user_profile = UserProfile.objects.get(user=instance.user)
            group.creator = user_profile
            group.created_by = user_profile.user  # Assuming created_by is a User field
            group.created_at = timezone.now()
            group.save()
        except UserProfile.DoesNotExist:
            # Handle the case where UserProfile does not exist for the user
            # You might want to create a UserProfile instance here or handle it based on your requirements
            pass

    

class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    completed = models.BooleanField(default=False)

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Update(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='updates')
    status = models.CharField(max_length=255)  # Assuming 'status' is the radio stage
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Update for {self.project.name} - {self.timestamp}'