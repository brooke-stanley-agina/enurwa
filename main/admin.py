from django.contrib import admin
from .models import (
    Destination, Package, PackageImage, Booking, Review, UserProfile, Testimonial, Safari, TourCategory, Contact, Blog, BlogComment
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

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'tour_type', 'duration', 'price', 'featured')
    list_filter = ('featured', 'tour_type', 'destination', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(PackageImage)
class PackageImageAdmin(admin.ModelAdmin):
    list_display = ('package', 'is_featured')
    list_filter = ('is_featured',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'travel_date', 'number_of_people', 'total_price', 'status', 'booking_date')
    list_filter = ('status', 'booking_date', 'travel_date')
    search_fields = ('user__username', 'user__email', 'package__name')
    readonly_fields = ('booking_date', 'total_price')

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
