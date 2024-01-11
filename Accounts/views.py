from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserProfile

# Create your views here.
@login_required
def user_profile_list(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'Accounts/user_profile_list.html', {'user_profiles': user_profiles})


from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth import login

def register_user(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']  # Set email in the User model
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # Log the user in
            login(request, user)

            return redirect('Accounts:homePage')  # Redirect to user profile list or any other page
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'Accounts/register_user.html', {'user_form': user_form, 'profile_form': profile_form})


from django.shortcuts import render, get_object_or_404
from .models import UserProfile

def user_detail(request, user_id):
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    return render(request, 'Accounts/user_detail.html', {'user_profile': user_profile})

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserProfileForm

@login_required
def edit_user(request):
    user = request.user
    profile = user.userprofile

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=profile)
        password_form = PasswordChangeForm(user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            messages.success(request, 'User details updated successfully!')
            return redirect('Accounts:user_detail', user.id)
    else:
        user_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeForm(user)

    return render(request, 'Accounts/edit_user.html', {'user_form': user_form, 'password_form': password_form})


# accounts/views.py
from django.contrib.auth.models import Group
from django.shortcuts import render
from .models import CustomGroup

def group_list(request):
    groups = CustomGroup.objects.all()
    return render(request, 'Accounts/group_list.html', {'groups': groups})

# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import GroupCreationForm
from .models import CustomGroup

# accounts/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import GroupCreationForm  # Update import here
from .models import CustomGroup

@login_required
def create_group(request):
    if request.method == 'POST':
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.created_by = request.user
            group.save()
            form.save_m2m()  # Save any many-to-many relationships

            # Add the group creator to the group
            group.user_set.add(request.user)

            return redirect('Accounts:group_list')
    else:
        form = GroupCreationForm()
    return render(request, 'Accounts/create_group.html', {'form': form})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group, User

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    all_users = User.objects.all()

    if request.method == 'POST':
        # Handle adding user to group
        if 'add_user_action' in request.POST:
            user_id = request.POST.get('add_user')  # Corrected name here
            user = get_object_or_404(User, id=user_id)
            group.user_set.add(user)

        # Handle removing user from group
        elif 'remove_user_action' in request.POST:
            user_id = request.POST.get('remove_user')
            user = get_object_or_404(User, id=user_id)
            group.user_set.remove(user)

        # Handle deleting the group
        elif 'delete_group_action' in request.POST:
            group.delete()
            return redirect('Accounts:group_list')

    return render(request, 'Accounts/group_detail.html', {'group': group, 'all_users': all_users})



# views.py
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('Accounts:group_list')






