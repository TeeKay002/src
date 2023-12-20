from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# models.py


class Project(models.Model):
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