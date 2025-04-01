from django.contrib import admin
from .models import (
    Destination, TourCategory, Package, PackageImage,
    Booking, Review, UserProfile, Testimonial
)

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'tour_type', 'price', 'duration')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('tour_type', 'destination', 'featured')
    search_fields = ('name', 'description')

admin.site.register(TourCategory)
admin.site.register(PackageImage)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(UserProfile)

# Add this to your existing admin.py registrations
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'rating', 'created_at', 'is_active')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'comment')
