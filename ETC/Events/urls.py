from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('form', views.form, name='form'),
    path('event_complete', views.event_complete, name='event_complete'),
    path('add_event_manager', views.add_event_manager, name='add_event_manager'),
    path('add_team_member', views.add_team_member, name='add_team_member'),
]
