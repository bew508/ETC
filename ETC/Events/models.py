from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model

CATEGORY_CHOICES = [
    (1, 'Musical'),
    (2, 'Play'),
    (3, 'Dance'),
    (4, 'Movie Night'),
    (5, 'Presentation'),
    (6, 'Open House'),
]

# Create your models here.
class EventCoordinator(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'
    
class Happening(models.Model):
    start_time = models.DateTimeField()
    duration = models.DurationField()
    
    def __str__(self):
        return f'{datetime.strftime(self.start_time, "%d.%m.%y %H:%M")} for {self.duration}'
    
class Event(models.Model):
    # Basic information
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    coordinator = models.ForeignKey(EventCoordinator, on_delete=models.CASCADE)
    manager = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, blank=True, null=True)
    team = models.ManyToManyField(get_user_model(), related_name='events', blank=True)
    
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=50)
    
    archived = models.BooleanField(default=False)
    
    rehearsals = models.ManyToManyField(Happening, related_name='events_rehearsals')
    performances = models.ManyToManyField(Happening, related_name='events_performances')
    
    def __str__(self):
        return f'{self.title} by {self.coordinator}'