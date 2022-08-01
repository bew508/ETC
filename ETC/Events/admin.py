from django.contrib import admin

from .models import EventCoordinator, Happening, Event

# Register your models here.
admin.site.register(EventCoordinator)
admin.site.register(Happening)
admin.site.register(Event)