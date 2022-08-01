from datetime import datetime, timedelta
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from .models import EventCoordinator, Happening, Event

CATEGORY_CHOICES = [
    'Musical',
    'Play',
    'Dance',
    'Movie Night',
    'Presentation',
    'Open House',
]

# Create your views here.
def index(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        return render(request, 'events/index.html')
    else:
        return redirect('events:form')
    
def form(request):
    if request.method == 'POST':
        # Try and find an existing event coordinator
        
        
        # Create new event coordinator
        try:
            coordinator = EventCoordinator.objects.create(email=request.POST['email'], last_name=request.POST['last'], first_name=request.POST['first'])
        except IntegrityError as e:
            print(e)
            return render(request, 'events/form.html', {
                'error': 'An error occured trying to create an EventCoordinator. Please try again later.'
            })
            
        # Check if rehearsal dates and times match
        print(request.POST)
        if len(request.POST.getlist('rehearsal-date')) != len(request.POST.getlist('rehearsal-time')):
            return render(request, 'events/form.html', {
                'error': 'Error on the amount of rehearsals.'
            })
            
        # Create all rehearsal happenings
        rehearsals = []
        for rehearsal in range(len(request.POST.getlist('rehearsal-date'))):
            try:
                date_time = datetime.strptime(request.POST.getlist('rehearsal-date')[rehearsal] + ' ' + request.POST.getlist('rehearsal-time')[rehearsal], '%Y-%m-%d %H:%M')
                duration = datetime.strptime(request.POST.getlist('rehearsal-duration')[rehearsal], '%H:%M')
                print(date_time)
                rehearsals.append(Happening.objects.create(start_time=date_time, duration=timedelta(hours=duration.hour, minutes=duration.minute)))
            except IntegrityError as e:
                print(e)
                return render(request, 'events/form.html', {
                    'error': 'An error occured trying to create a rehearsal Happening. Please try again later.'
                })
                
        # Check if performance dates and times match
        if len(request.POST.getlist('performance-date')) != len(request.POST.getlist('performance-time')):
            return render(request, 'events/form.html', {
                'error': 'Error on the amount of performances.'
            })
            
        # Create all performance happenings
        performances = []
        for performance in range(len(request.POST.getlist('performance-date'))):
            try:
                date_time = datetime.strptime(request.POST.getlist('performance-date')[performance] + ' ' + request.POST.getlist('performance-time')[performance], '%Y-%m-%d %H:%M')
                duration = datetime.strptime(request.POST.getlist('performance-duration')[performance], '%H:%M')
                print(date_time)
                performances.append(Happening.objects.create(start_time=date_time, duration=timedelta(hours=duration.hour, minutes=duration.minute)))
            except IntegrityError as e:
                print(e)
                return render(request, 'events/form.html', {
                    'error': 'An error occured trying to create a performance Happening. Please try again later.'
                })
        
        # Create new event
        try:
            event = Event.objects.create(
                title = request.POST.get('title'),
                coordinator = coordinator,
                category = 'None', # TODO
                location = 'None', # TODO
            )
            event.rehearsals.set(rehearsals)
            event.performances.set(performances)
            event.save()
        except IntegrityError as e:
            print(e)
            return render(request, 'events/form.html', {
                'error': 'An error occured trying to create an Event. Please try again later.'
            })
        
        print(request.POST)
        
        return render(request, 'events/form_review.html')
        
    else:
        # Return form page
        return render(request, 'events/form.html')

