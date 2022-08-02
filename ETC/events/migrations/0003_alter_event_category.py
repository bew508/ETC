# Generated by Django 4.0.6 on 2022-08-01 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_eventcoordinator_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('0', 'Musical'), ('1', 'Play'), ('2', 'Dance'), ('3', 'Movie Night'), ('4', 'Presentation'), ('5', 'Open House')], max_length=1),
        ),
    ]