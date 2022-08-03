import json
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import redirect, render
from regex import W

from .models import COMMON_ROLE_CHOICES, UNIQUE_ROLE_CHOICES

from .decorators import unique_role_required

# Create your views here.
@login_required
def index(request):
    return render(request, 'users/index.html')

def login_view(request):
    def activate(id, activate_form):
        def post():
            # Get user
            user = get_user_model().objects.get(pk=id)
            
            # Get form fields
            password = request.POST.get('password')
            confirm = request.POST.get('confirm-password')
            
            # Check for match
            if password != confirm:
                return 'Passwords do not match'
            
            # Check for valid password (secure)
            try:
                validate_password(password, user)
            except ValidationError as error:
                return error
            
            # Set as new password
            user.set_password(password)
            user.save()
            
            # Set account as activated
            user.activated = True
            user.save()
            
            # Login user
            login(request, user)
            
            return ''
            
        if activate_form:
            error = post()
            
            if not error:
                return redirect('home:index')
            
        else:
            error = ''
                        
        return render(request, 'users/activate.html', {
            'errors': [error] if type(error) is str else error,
            'id': id
        })
    
    # Check for logged in users
    if request.user.is_authenticated:
        return redirect('home:index')
    
    if request.method == 'POST':
        
        # Log user in
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        # Get activate form results
        id = request.POST.get('id')
        
        # Check for activate form
        if id:
            return activate(id, True)

        # Check if authentication successful
        if user:
            # Check for unactivated users
            if not user.activated:
                return activate(user.id, False)
            
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

@unique_role_required()
def list(request):    
    return render(request, 'users/user_list.html', {
        'users': get_user_model().objects.all()
    })

@unique_role_required()
def create_account(request):
    def post():
        # Get fields from form
        first = request.POST.get('first')
        last = request.POST.get('last')
        email = request.POST.get('email')
        unique_role = request.POST.get('unique-role')
        common_role = request.POST.get('common-role')
        
        # Convert unique_role
        unique_role = None if len(unique_role) == 0 else unique_role
        
        # Return errors for existing username or email
        if get_user_model().objects.filter(email=email).first():
            return 'This email is alreay taken.'

        # Attempt to create new user
        try:
            get_user_model().objects.create_user(first, last, email, unique_role=unique_role, common_role=common_role)
        except IntegrityError as e:
            print(e)
            return 'An error occured. Please try again later.'
        
        # Send user an email
        send_mail(
            subject='ETC Website Account',
            message=
            f"""
            An account has just been created for you on the ETC Website! Use the following login information to log in:
            
            Email: {email}
            Password: {first.lower()}.{last.lower()}
            
            You will be prompted to change your password once you log in for the first time.
            """,
            from_email=None,
            recipient_list=[email]
        )
            
        return ''
    
    if request.method == 'POST':
        error = post()
        
        if not error:
            # Go to users list view
            return redirect('users:list')
    else:
        error = ''
        
    return render(request, 'users/create_account.html', {
        'error': error,
        'unique_roles_available': [role for role in UNIQUE_ROLE_CHOICES if not get_user_model().objects.filter(unique_role=role[0])],
        'common_roles_available': COMMON_ROLE_CHOICES,
    })
    
@unique_role_required()
@require_POST
def remove(request):
    # Get user
    user = get_user_model().objects.get(pk=json.loads(request.body).get('id'))
    
    # Delete user
    user.delete()
    
    return redirect('users:list')