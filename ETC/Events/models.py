from django.db import models

# Create your models here.
class EventCoordinator(models.Model):
    email = models.EmailField(max_length=254)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    
class Happening(models.Model):
    start_time = models.DateTimeField()
    duration = models.DurationField()
    
class Event(models.Model):
    # Basic information
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    coordinator = models.ForeignKey(EventCoordinator, on_delete=models.CASCADE)
    
    category = models.CharField(max_length=50, choices=[])
    location = models.CharField(max_length=50)
    
    rehearsals = models.ManyToManyField(Happening)
    performances = models.ManyToManyField(Happening)