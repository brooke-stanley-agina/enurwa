# Generated by Django 5.0.3 on 2025-05-10 20:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_booking_preferred_package_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='itinerary',
        ),
        migrations.RemoveField(
            model_name='package',
            name='price',
        ),
        migrations.AddField(
            model_name='package',
            name='overview',
            field=models.TextField(blank=True, help_text='A brief overview of the package', null=True),
        ),
        migrations.CreateModel(
            name='DayItinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('accommodation', models.CharField(max_length=200)),
                ('meals', models.CharField(help_text="e.g., 'Breakfast, Lunch, Dinner'", max_length=200)),
                ('activities', models.TextField(help_text='List of activities for the day')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='daily_itinerary', to='main.package')),
            ],
            options={
                'verbose_name_plural': 'Day Itineraries',
                'ordering': ['day_number'],
            },
        ),
    ]
