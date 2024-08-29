from django.shortcuts import render, redirect
from django.contrib import messages
from . forms import RegForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def register(request):
    if request.method == "POST":
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully you can now login.')
            return redirect('login')
    else:
        form = RegForm()
    
    return render(request, 'Users/registration.html', {'form': form})

@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Account updated successfully.')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'Users/profile.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'Users/logout.html')
