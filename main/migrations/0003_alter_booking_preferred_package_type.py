# Generated by Django 5.0.3 on 2025-05-10 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_booking_accommodation_preference_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='preferred_package_type',
            field=models.CharField(choices=[('adventure', 'Adventure'), ('honeymoon', 'Honeymoon'), ('family', 'Family'), ('luxury', 'Luxury'), ('budget', 'Budget')], max_length=20),
        ),
    ]
