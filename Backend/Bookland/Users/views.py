from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def profile(request):
    return render(request, 'Users/manage_profile.html')


@login_required
def edit_profile(request):
    edit_profile_msg = ''
    if request.method == 'POST':
        user_form = UserForm(request.POST,
                             instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully')
            return redirect('manage-profile')
        else:
            # edit_profile_msg = 'Username is already taken'
            return redirect('edit-profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)
    context = {
        # 'edit_profile_msg': edit_profile_msg,
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'Users/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('manage-profile')

    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'Users/change_password.html', context)
