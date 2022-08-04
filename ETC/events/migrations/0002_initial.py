# Generated by Django 4.0.6 on 2022-08-04 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='performances',
            field=models.ManyToManyField(related_name='events_performances', to='events.happening'),
        ),
        migrations.AddField(
            model_name='event',
            name='rehearsals',
            field=models.ManyToManyField(related_name='events_rehearsals', to='events.happening'),
        ),
        migrations.AddField(
            model_name='event',
            name='team',
            field=models.ManyToManyField(blank=True, related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
