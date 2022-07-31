from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.
def login_view(request):
    # Check for logged in users
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':
        
        # Log user in
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            # Log in user
            login(request, user)
            return redirect('home:index')
        else:
            return render(request, 'users/login.html', {
                'error': 'Invalid email and/or password.'
            })
            
    else:
        return render(request, 'users/login.html')
    
    
def logout_view(request):
    # Log user out
    logout(request)
    return redirect('home:index')


def register(request):
    # Check for logged in users
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':
        
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'users/register.html', {
                'error': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, 'users/register.html', {
                'message': 'Email address already taken.'
            })
        login(request, user)
        return redirect('home:index')
    
    else:
        return render(request, 'users/register.html')