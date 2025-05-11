from django.contrib import admin
from .models import (
    Destination, Package, PackageImage, Booking, Review, UserProfile, Testimonial, Safari, 
    TourCategory, Contact, Blog, BlogComment, DayItinerary
)

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'featured', 'created_at')
    list_filter = ('featured', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image', 'featured')
        }),
        ('Detailed Information', {
            'fields': ('wildlife_info', 'best_time_to_visit', 'travel_tips')
        }),
        ('Location Details', {
            'fields': ('location', 'time_zone', 'climate', 'nearest_airport')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    readonly_fields = ('created_at', 'updated_at')

class DayItineraryInline(admin.TabularInline):
    model = DayItinerary
    extra = 1
    ordering = ['day_number']

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'tour_type', 'duration', 'featured')
    list_filter = ('tour_type', 'destination', 'featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DayItineraryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'destination', 'category', 'tour_type')
        }),
        ('Package Details', {
            'fields': ('overview', 'description', 'duration', 'max_group_size', 'featured')
        }),
        ('Package Inclusions/Exclusions', {
            'fields': ('inclusions', 'exclusions')
        })
    )

@admin.register(DayItinerary)
class DayItineraryAdmin(admin.ModelAdmin):
    list_display = ('day_title', 'package', 'day_number', 'accommodation', 'meals')
    list_filter = ('package', 'accommodation')
    search_fields = ('title', 'description', 'activities', 'package__name')
    ordering = ['package', 'day_number']
    
    def day_title(self, obj):
        return f'Day {obj.day_number}: {obj.title}'
    day_title.short_description = 'Day Itinerary'
    
    fieldsets = (
        ('Package Information', {
            'fields': ('package', 'day_number', 'title')
        }),
        ('Day Details', {
            'fields': ('description', 'activities')
        }),
        ('Accommodation & Meals', {
            'fields': ('accommodation', 'meals')
        })
    )

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ('package', 'is_featured')
    list_filter = ('is_featured',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'package', 'start_date', 'total_guests', 'status')
    list_filter = ('status', 'preferred_package_type', 'country')
    search_fields = ('full_name', 'email', 'phone', 'package__name')
    readonly_fields = ('booking_date',)

    def total_guests(self, obj):
        return obj.adults + obj.children
    total_guests.short_description = 'Total Guests'

    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone', 'country')
        }),
        ('Package Details', {
            'fields': ('package', 'preferred_package_type')
        }),
        ('Trip Details', {
            'fields': ('start_date', 'end_date', 'adults', 'children', 'special_requirements')
        }),
        ('Booking Status', {
            'fields': ('status', 'total_price', 'booking_date')
        })
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'package__name', 'comment')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'nationality')
    search_fields = ('user__username', 'user__email', 'phone', 'nationality')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('name', 'country', 'comment')

@admin.register(Safari)
class SafariAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active', 'created_at')
    search_fields = ('name', 'description')

@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'featured', 'created_at', 'views')
    list_filter = ('status', 'featured', 'created_at', 'author')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'image')
        }),
        ('Additional Information', {
            'fields': ('excerpt', 'featured', 'status', 'views')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('blog', 'author', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'blog__title', 'author__username')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
