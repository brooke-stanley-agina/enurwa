from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from cloudinary.models import CloudinaryField

class Destination(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = CloudinaryField('image', folder='destinations')
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional fields for detailed information
    wildlife_info = models.TextField(blank=True)
    best_time_to_visit = models.TextField(blank=True)
    travel_tips = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    time_zone = models.CharField(max_length=100, blank=True)
    climate = models.CharField(max_length=200, blank=True)
    nearest_airport = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']

class TourCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class DayItinerary(models.Model):
    package = models.ForeignKey('Package', related_name='daily_itinerary', on_delete=models.CASCADE)
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    accommodation = models.CharField(max_length=200)
    meals = models.CharField(max_length=200, help_text="e.g., 'Breakfast, Lunch, Dinner'")
    activities = models.TextField(help_text="List of activities for the day")
    
    class Meta:
        ordering = ['day_number']
        verbose_name_plural = 'Day Itineraries'
    
    def __str__(self):
        return f"{self.package.name} - Day {self.day_number}: {self.title}"

class Package(models.Model):
    TOUR_TYPES = [
        ('adventure', 'Adventure'),
        ('honeymoon', 'Honeymoon'),
        ('family', 'Family'),
        ('luxury', 'Luxury'),
        ('budget', 'Budget'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    category = models.ForeignKey(TourCategory, on_delete=models.SET_NULL, null=True)
    tour_type = models.CharField(max_length=20, choices=TOUR_TYPES)
    description = models.TextField()
    overview = models.TextField(help_text="A brief overview of the package", blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    max_group_size = models.PositiveIntegerField(default=6, help_text="Maximum number of people allowed in a group")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per person in USD", default=0)
    featured = models.BooleanField(default=False)
    inclusions = models.TextField()
    exclusions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PackageImage(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder='packages')
    is_featured = models.BooleanField(default=False)

import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    # Use the same tour types as Package model
    PACKAGE_TYPE_CHOICES = Package.TOUR_TYPES

    # Booking identifier
    booking_id = models.CharField(max_length=50, unique=True, null=True, blank=True, editable=False)

    # User and Package
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
    
    # Contact Information
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    
    # Booking Details
    booking_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default='2025-05-10')
    end_date = models.DateField(default='2025-05-10')
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    preferred_package_type = models.CharField(max_length=20, choices=PACKAGE_TYPE_CHOICES)
    special_requirements = models.TextField(blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        package_str = self.package.name if self.package else 'No Package'
        return f"Booking by {user_str} for {package_str}"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        package_str = self.package.name if self.package else 'No Package'
        return f"Review by {user_str} for {package_str}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    nationality = models.CharField(max_length=100)
    profile_picture = CloudinaryField('image', folder='profiles', null=True, blank=True)

    def __str__(self):
        return self.user.username

# Add this model to your existing models.py
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    image = CloudinaryField('image', folder='testimonials', null=True, blank=True)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Testimonial by {self.name}"

class Safari(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', folder='package_images', blank=True, null=True)
    included_services = models.TextField(help_text="List of services included in the package")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Safari Package'
        verbose_name_plural = 'Safari Packages'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', null=True, blank=True)
    excerpt = models.TextField(max_length=200, blank=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('published', 'Published')
    ], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.excerpt:
            self.excerpt = self.content[:200] + '...'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        author_str = self.author.username if self.author else 'Anonymous'
        blog_str = self.blog.title if self.blog else 'No Blog'
        return f'Comment by {author_str} on {blog_str}'

    class Meta:
        ordering = ['-created_at']
