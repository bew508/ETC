from datetime import datetime, timedelta
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .models import EventCoordinator, Happening, Event, CATEGORY_CHOICES

# Create your views here.
def index(request):
    # Check if user is logged in
    if request.user.is_authenticated:
        return render(request, 'events/index.html')
    else:
        return redirect('events:form')
    
def form(request):
    def post():
        print(request.POST)
        
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
                print(date_time)
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
                print(date_time)
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

