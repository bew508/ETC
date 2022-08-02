from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render

# Create your views here.
@login_required
def index(request):
    return render(request, 'users/index.html')

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
    
@login_required
def logout_view(request):
    # Log user out
    logout(request)
    return redirect('home:index')


def register(request):
    # Check for logged in users
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':
        
        username = request.POST['new-username']
        email = request.POST['new-email']

        # Ensure password matches confirmation
        password = request.POST['new-password']
        confirmation = request.POST['new-password-confirmation']
        if password != confirmation:
            return render(request, 'users/register.html', {
                'error': 'Passwords do not match.'
            })

        # Return errors for existing username or email
        if len(User.objects.filter(username=username)) > 0:
            return render(request, 'users/register.html', {
                'error': 'This username is alreay taken.'
            })
        if len(User.objects.filter(email=email)) > 0:
            return render(request, 'users/register.html', {
                'error': 'This email is alreay taken.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, 'users/register.html', {
                'error': 'An error occured. Please try again later.'
            })
            
        # Log in user
        login(request, user)
        return redirect('home:index')
    
    else:
        return render(request, 'users/register.html')