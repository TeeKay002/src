from email.headerregistry import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Comment, Task, UserActivity, Update
from .forms import ProjectForm, UpdateForm
from guardian.shortcuts import get_objects_for_user
from project_manager.models import Project  # Adjust this import based on your project structure
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user
from guardian.mixins import PermissionRequiredMixin
from .models import UserProfile, CustomGroup
from django.utils import timezone




@login_required
def project_list(request):
    # Retrieve projects for which the user has view permission
    projects = get_objects_for_user(
        request.user,
        'view_project',
        klass=Project,
        accept_global_perms=False,
        with_superuser=False
    )

    print("User:", request.user)
    print("Projects:", projects)

    return render(request, 'project_manager/project_list.html', {'projects': projects})



@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    PermissionRequiredMixin().check_object_permissions(request, project)
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
            'user': update.user,  # Use the user from the update object
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
        'user': project.user,
    })



@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()

            # Retrieve the UserProfile for the current user
            try:
                user_profile = UserProfile.objects.get(user=request.user)

                # Create UserActivity associated with UserProfile
                UserActivity.objects.create(user=user_profile.user, project=project, activity_type='created')

                # Create or retrieve CustomGroup and set created_by and created_at
                group_name = f"{project.name}"
                group, created = CustomGroup.objects.get_or_create(name=group_name)
                group.creator = user_profile
                group.created_by = user_profile.user  # Assuming created_by is a User field
                group.created_at = timezone.now()
                group.save()

                # Add the creator to the group and grant additional permissions
                group.user_set.add(request.user)
                assign_perm('change_project', request.user, project)
                assign_perm('delete_project', request.user, project)

            except UserProfile.DoesNotExist:
                # Handle the case where UserProfile does not exist for the user
                # You might want to create a UserProfile instance here or handle it based on your requirements
                pass

            return redirect('project_manager:project_list')

    else:
        form = ProjectForm()

    return render(request, 'project_manager/project_create.html', {'form': form})



@login_required
def add_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            new_update = form.save(commit=False)
            new_update.project = project
            new_update.user = request.user  # Set the user field to the current user

            # Update project status and description
            project.status = new_update.status
            project.description = new_update.description

            new_update.save()
            project.already_paid += new_update.amount_paid
            project.save()

            return redirect('project_manager:project_detail', project_id=project.id)
    else:
        form = UpdateForm()

    return render(request, 'project_manager/add_update.html', {'project': project, 'form': form})