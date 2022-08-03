from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model

from .models import UNIQUE_ROLE_CHOICES, COMMON_ROLE_CHOICES

def minimum_role_required(role):
    """
    Decorator for views that checks that the user is logged in and has the appropriate role.
    """
    def check_role(user):
        # Check that user is logged in
        if not user.is_authenticated:
            raise PermissionDenied
        
        # Get user
        user = get_user_model().objects.get(pk=user.pk)
        
        # Check for a unique role
        is_unique_role = any(role in tuple for tuple in UNIQUE_ROLE_CHOICES)
        
        # Check if it is a role at all
        if not is_unique_role and not any(role in tuple for tuple in COMMON_ROLE_CHOICES):
            raise ValueError(f"'{role}' is not a valid role")
        
        # Unique roles can access any common role only view
        if not is_unique_role and user.unique_role:
            return True

        # Users with no unique roles can't access unique only view
        if is_unique_role and not user.unique_role:
            raise PermissionDenied
                
        # Check that user has at least the required role
        if (user.unique_role if is_unique_role else user.common_role) <= [tuple[0] for tuple in (UNIQUE_ROLE_CHOICES if is_unique_role else COMMON_ROLE_CHOICES) if tuple[1] == role].pop():
            return True
        else:
            raise PermissionDenied

    # Return the test
    return user_passes_test(check_role)

def unique_role_required():
    """
    Decorator for views that checks that the user ifs logged in and has a unique role.
    """
    return minimum_role_required(UNIQUE_ROLE_CHOICES[-1][1])