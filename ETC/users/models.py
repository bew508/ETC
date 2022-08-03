from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager

UNIQUE_ROLE_CHOICES = [
    (1, 'Teacher Sponsor'),
    (2, 'Technical Director'),
    (3, 'Technical Deputy Director'),
]

COMMON_ROLE_CHOICES = [
    (1, 'Senior Member'),
    (2, 'Member'),
    (3, 'Applicant')
]
    
class User(AbstractUser):
    # Set custom manager
    objects = UserManager()
    
    # Set new username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Override AbstractUser fields
    username = None
    email = models.EmailField(unique=True)
    
    # Field to store whether the account has been activated by the user
    activated = models.BooleanField(default=False)
    
    unique_role = models.PositiveSmallIntegerField(choices=UNIQUE_ROLE_CHOICES, unique=True, blank=True, null=True)
    common_role = models.PositiveSmallIntegerField(choices=COMMON_ROLE_CHOICES)
        
    def __str__(self):
        if self.unique_role:
            role = f'{self.get_unique_role_display()} ({self.get_common_role_display()})'
        else:
            role = self.get_common_role_display()
        return f'{self.first_name} {self.last_name} - {role}'
