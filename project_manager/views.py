from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

    

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Comment, Task, UserActivity, Update
from .forms import ProjectForm, UpdateForm

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_manager/project_list.html', {'projects': projects})

from datetime import datetime

from django.shortcuts import render, get_object_or_404
from .models import Project, Comment, Task, UserActivity

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    comments = Comment.objects.filter(project=project)
    tasks = Task.objects.filter(project=project)
    activities = UserActivity.objects.filter(project=project)

    # Split the stages string into a list
    stages = project.stages.split(',') if project.stages else []

    # Calculate the balance in the view
    amount_needed = project.amount_needed or 0.0
    already_paid = project.already_paid or 0.0
    balance = amount_needed - already_paid

    # Create a list to store the stages with timestamps
    stage_with_timestamp = []

    # Iterate through updates and append relevant information
    for update in project.updates.all():  # Use the related name 'updates'
        stage_with_timestamp.append({
            'stage': update.status,
            'timestamp': update.timestamp,
            'amount_paid': update.amount_paid,
            'description': update.description,
        })

    return render(request, 'project_manager/project_detail.html', {
        'project': project,
        'comments': comments,
        'tasks': tasks,
        'stages': stages,
        'balance': balance,
        'stage_with_timestamp': stage_with_timestamp,
    })




def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            UserActivity.objects.create(user=request.user, project=project, activity_type='created')
            return redirect('project_manager:project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_manager/project_create.html', {'form': form})


# project_manager/views.py
from django.shortcuts import get_object_or_404, render, redirect
from .models import Project
from .forms import UpdateForm  # Assuming you have a form for handling updates

def add_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            new_update = form.save(commit=False)
            new_update.project = project
            new_update.save()
            return redirect('project_manager:project_detail', project_id=project.id)
    else:
        form = UpdateForm()

    return render(request, 'project_manager/add_update.html', {'project': project, 'form': form})
