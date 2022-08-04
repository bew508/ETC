from datetime import datetime, timedelta
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from users.decorators import unique_role_required

from .models import EventCoordinator, Happening, Event, CATEGORY_CHOICES

# Create your views here.
def index(request):    
    # Check if user is logged in
    if request.user.is_authenticated:
        # Set upcoming events
        if request.user.unique_role != None:
            upcoming_events = Event.objects.filter(archived=False).order_by('created_at')
            past_events = Event.objects.filter(archived=True).order_by('-created_at')
            staff_view = True
        else:
            upcoming_events = Event.objects.filter(archived=False, team__id=request.user.id).order_by('created_at')
            past_events = Event.objects.filter(archived=True, team__id=request.user.id).order_by('-created_at')
            staff_view = False
        
        return render(request, 'events/index.html', {
            'upcoming_events': upcoming_events,
            'past_events': past_events,
            'users': get_user_model().objects.all() if staff_view else [],
            'staff_view': staff_view,
        })
    else:
        return redirect('events:form')
    
def form(request):
    def post():        
        # Try and find an existing event coordinator
        coordinator = EventCoordinator.objects.filter(email=request.POST.get('email')).first()
        if coordinator:
            # Check if first and last name match
            if coordinator.first_name != request.POST.get('first'):
                return 'First name does not match email address.'
            if coordinator.last_name != request.POST.get('last'):
                return 'Last name does not match email address.'
        
        # Create new event coordinator
        else:
            try:
                coordinator = EventCoordinator.objects.create(
                    email=request.POST.get('email'), 
                    last_name=request.POST.get('last'), 
                    first_name=request.POST.get('first')
                )
            except IntegrityError as e:
                print(e)
                return 'An error occured trying to create an EventCoordinator object. Please try again later.'
            
        # Check if rehearsal dates and times match
        if len(request.POST.getlist('rehearsal-date')) != len(request.POST.getlist('rehearsal-time')):
            return 'Error on the amount of rehearsals.'
            
        # Create all rehearsal happenings
        rehearsals = []
        for rehearsal in range(len(request.POST.getlist('rehearsal-date'))):
            try:
                date_time = datetime.strptime(
                    request.POST.getlist('rehearsal-date')[rehearsal]
                    + ' ' + 
                    request.POST.getlist('rehearsal-time')[rehearsal]
                    , '%Y-%m-%d %H:%M')
                duration = datetime.strptime(request.POST.getlist('rehearsal-duration')[rehearsal], '%H:%M')
                rehearsals.append(Happening.objects.create(start_time=date_time, duration=timedelta(hours=duration.hour, minutes=duration.minute)))
            except IntegrityError as e:
                print(e)
                return 'An error occured trying to create a rehearsal Happening object. Please try again later.'
                
        # Check if performance dates and times match
        if len(request.POST.getlist('performance-date')) != len(request.POST.getlist('performance-time')):
            return 'Error on the amount of performances.'
            
        # Create all performance happenings
        performances = []
        for performance in range(len(request.POST.getlist('performance-date'))):
            try:
                date_time = datetime.strptime(
                    request.POST.getlist('performance-date')[performance]
                    + ' ' +
                    request.POST.getlist('performance-time')[performance]
                    , '%Y-%m-%d %H:%M'
                    )
                duration = datetime.strptime(request.POST.getlist('performance-duration')[performance], '%H:%M')
                performances.append(Happening.objects.create(start_time=date_time, duration=timedelta(hours=duration.hour, minutes=duration.minute)))
            except IntegrityError as e:
                print(e)
                return 'An error occured trying to create a performance Happening object. Please try again later.'
        
        # Create new event
        try:
            event = Event.objects.create(
                title = request.POST.get('title'),
                coordinator = coordinator,
                category = request.POST.get('category'),
                location = request.POST.get('location'),
            )
            event.rehearsals.set(rehearsals)
            event.performances.set(performances)
            event.save()
        except IntegrityError as e:
            print(e)
            return 'An error occured trying to create an Event object. Please try again later.'
                
        return ''
        
    if request.method == 'POST':
        # Run post function
        error = post()
        
        # Move to form_review in case of no error
        if not error:
            return render(request, 'events/form_review.html', {
                'form': {
                    'first': request.POST.get('first', ''),
                    'last': request.POST.get('last', ''),
                    'email': request.POST.get('email', ''),
                    'title': request.POST.get('title', ''),
                    'category': CATEGORY_CHOICES[int(request.POST.get('category', ''))][1],
                    'location': request.POST.get('location', ''),
                    'rehearsal_count': range(len(request.POST.getlist('rehearsal-date'))),
                    'rehearsal_date': request.POST.getlist('rehearsal-date', ''),
                    'rehearsal_time': request.POST.getlist('rehearsal-time', ''),
                    'rehearsal_duration': request.POST.getlist('rehearsal-duration', ''),
                    'performance_count': range(len(request.POST.getlist('performance-date'))),
                    'performance_date': request.POST.getlist('performance-date', ''),
                    'performance_time': request.POST.getlist('performance-time', ''),
                    'performance_duration': request.POST.getlist('performance-duration', ''),
                }
            })

        # Set first, last, and email to form data        
        first = request.POST.get('first', '')
        last = request.POST.get('last', '')
        email = request.POST.get('email', '')
        
    else:
        error = ''
        
        # Autofill first, last, and email with logged in user
        if request.user.is_authenticated:
            first = request.user.first_name
            last = request.user.last_name
            email = request.user.email
        else:
            first = ''
            last = ''
            email = ''
            
    # Return form page
    return render(request, 'events/form.html', {
        'error': error,
        'category_choices': CATEGORY_CHOICES,
        'form': {
            'first': first,
            'last': last,
            'email': email,
            'title': request.POST.get('title', ''),
            'category': request.POST.get('category', ''),
            'location': request.POST.get('location', ''),
            'rehearsal_count': range(len(request.POST.getlist('rehearsal-date'))),
            'rehearsal_date': request.POST.getlist('rehearsal-date', ''),
            'rehearsal_time': request.POST.getlist('rehearsal-time', ''),
            'rehearsal_duration': request.POST.getlist('rehearsal-duration', ''),
            'performance_count': range(len(request.POST.getlist('performance-date'))),
            'performance_date': request.POST.getlist('performance-date', ''),
            'performance_time': request.POST.getlist('performance-time', ''),
            'performance_duration': request.POST.getlist('performance-duration', ''),
        }
    })


@require_POST
@unique_role_required()
def event_complete(request):
    # Get event
    id = request.POST.get('id')
    event = Event.objects.get(pk=id)
    
    # Mark event as archived
    event.archived = True
    event.save()
    
    return redirect('events:index')
    
    
@require_POST
@unique_role_required()
def add_event_manager(request):
    # Get event
    event_id = request.POST.get('event-id')
    event = Event.objects.get(pk=event_id)
    
    # Get user
    user_id = request.POST.get('event-manager')
    user = get_user_model().objects.get(pk=user_id)
    
    # Assign event manager
    event.manager = user
    event.save()
    
    return redirect('events:index')

@require_POST
@unique_role_required()
def add_team_member(request):
    # Get event
    event_id = request.POST.get('event-id')
    event = Event.objects.get(pk=event_id)
    
    for user in request.POST.getlist('team-members'):
        # Add all users to team
        event.team.add(user)
    
    return redirect('events:index')