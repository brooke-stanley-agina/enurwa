from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import Destination, Package, Testimonial, Booking, Contact, PackageImage, Review, UserProfile, Safari, TourCategory, Blog, BlogComment
from .forms import BookingForm, BlogForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

def home(request):
    featured_destinations = Destination.objects.filter(featured=True)[:6]
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'main/index.html', {
        'featured_destinations': featured_destinations,
        'testimonials': testimonials,
        'package_types': Package.TOUR_TYPES
    })

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    packages = Package.objects.filter(destination=destination)
    return render(request, 'main/destination_detail.html', {
        'destination': destination,
        'packages': packages
    })

def package_detail(request, slug):
    package = get_object_or_404(
        Package.objects.prefetch_related('daily_itinerary', 'images'),
        slug=slug
    )
    related_packages = Package.objects.filter(
        destination=package.destination
    ).exclude(
        id=package.id
    ).prefetch_related(
        'images'
    )[:3]
    
    return render(request, 'main/package_detail.html', {
        'package': package,
        'related_packages': related_packages,
        'today': timezone.now().date(),
        'package_types': Package.TOUR_TYPES
    })

def about(request):
    testimonials = Testimonial.objects.all()[:4]
    return render(request, 'main/about.html', {
        'testimonials': testimonials
    })

def destinations(request):
    destinations = Destination.objects.all()
    return render(request, 'main/destinations.html', {
        'destinations': destinations
    })

def packages(request):
    packages = Package.objects.all().prefetch_related('daily_itinerary').order_by('?')
    tour_type = request.GET.get('tour_type')
    featured = request.GET.get('featured')
    destination = request.GET.get('destination')

    if tour_type:
        packages = packages.filter(tour_type=tour_type)
    if featured:
        packages = packages.filter(featured=True)
    if destination:
        packages = packages.filter(destination__slug=destination)

    return render(request, 'main/packages.html', {
        'packages': packages,
        'tour_types': Package.TOUR_TYPES,
        'destinations': Destination.objects.all()
    })

def blog(request):
    return render(request, 'main/blog.html')

def contact(request):
    if request.method == 'POST':
        try:
            contact = Contact.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message')
            )
            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('contact')
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
            return redirect('contact')
    return render(request, 'main/contact.html')

def book(request):
    if request.method == 'POST':
        # Create booking
        package_id = request.POST.get('package')
        package = Package.objects.get(id=package_id)
        booking = Booking.objects.create(
            user=request.user,
            package=package,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            adults=int(request.POST.get('adults', 1)),
            children=int(request.POST.get('children', 0)),
            accommodation_preference=request.POST.get('accommodation'),
            special_requirements=request.POST.get('special_requirements', ''),
            total_price=0,  # Price will be determined after inquiry
            status='pending'
        )
        messages.success(request, 'Your booking has been created successfully!')
        return redirect('booking_detail', id=booking.id)
    return render(request, 'main/book.html')

import json

@csrf_exempt
def booking_create(request):
    if request.method == 'POST':
        try:
            # Try to get data from request body (API calls)
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                # If not JSON, use POST data (form submission)
                data = request.POST

            # Get the package
            package_id = data.get('package')
            if not package_id:
                return JsonResponse({'error': 'Package ID is required'}, status=400)
            
            try:
                package = Package.objects.get(id=package_id)
            except Package.DoesNotExist:
                return JsonResponse({'error': 'Invalid package ID'}, status=400)

            # Validate required fields
            required_fields = ['full_name', 'email', 'phone', 'country', 'start_date', 'end_date']
            for field in required_fields:
                if not data.get(field):
                    if request.content_type == 'application/json':
                        return JsonResponse({'error': f'Missing required field: {field}'}, status=400)
                    messages.error(request, f'Please provide your {field.replace("_", " ").title()}')
                    return redirect('package_detail', slug=package.slug)

            # Create the booking
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                package=package,
                # Contact Information
                full_name=data.get('full_name'),
                email=data.get('email'),
                phone=data.get('phone'),
                country=data.get('country'),
                # Trip Details
                start_date=data.get('start_date'),
                end_date=data.get('end_date'),
                adults=int(data.get('adults', 1)),
                children=int(data.get('children', 0)),
                preferred_package_type=data.get('preferred_package_type'),
                special_requirements=data.get('special_requests', ''),
                status='pending'
            )

            # Get existing booking IDs from cookies
            booking_ids = request.COOKIES.get('booking_ids', '')
            booking_id_list = booking_ids.split(',') if booking_ids else []
            
            # Add new booking ID
            booking_id_list.append(str(booking.booking_id))
            
            # Return JSON response for API calls
            if request.content_type == 'application/json':
                response = JsonResponse({
                    'message': 'Booking request submitted successfully',
                    'booking_id': booking.booking_id,
                    'redirect_url': reverse('my_bookings')
                })
            else:
                # Redirect to my bookings page
                messages.success(request, 'Your booking request has been submitted successfully!')
                response = redirect('my_bookings')
            
            # Set cookie with updated booking IDs
            response.set_cookie('booking_ids', ','.join(booking_id_list), max_age=365*24*60*60)  # 1 year expiry
            
            return response

        except Exception as e:
            print('Error creating booking:', str(e))
            if request.content_type == 'application/json':
                return JsonResponse({'error': str(e)}, status=400)
            messages.error(request, 'There was an error processing your booking. Please try again.')
            return redirect('package_detail', slug=package.slug)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def my_bookings(request):
    booking_ids = request.COOKIES.get('booking_ids', '')
    if booking_ids:
        booking_ids = booking_ids.split(',')
        bookings = Booking.objects.filter(booking_id__in=booking_ids).order_by('-booking_date')
    else:
        bookings = []
    return render(request, 'main/my_bookings.html', {'bookings': bookings})

@login_required
def booking_detail(request, id):
    booking = get_object_or_404(Booking, id=id, user=request.user)
    return render(request, 'main/booking_detail.html', {'booking': booking})

@login_required
def booking_cancel(request, id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=id, user=request.user)
        if booking.status == 'pending':
            booking.status = 'cancelled'
            booking.save()
            messages.success(request, 'Your booking has been cancelled successfully.')
        else:
            messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', id=booking.id)
    return redirect('home')

def blog_list(request):
    blogs = Blog.objects.filter(status='published')
    featured_blogs = Blog.objects.filter(featured=True, status='published')[:3]
    context = {
        'blogs': blogs,
        'featured_blogs': featured_blogs,
    }
    return render(request, 'main/blog_list.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    comments = blog.comments.all()
    
    # Increment view count
    blog.views += 1
    blog.save()
    
    context = {
        'blog': blog,
        'comments': comments,
    }
    return render(request, 'main/blog_detail.html', context)

@login_required
def blog_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            BlogComment.objects.create(
                blog=blog,
                author=request.user,
                content=content
            )
            messages.success(request, 'Your comment has been added successfully!')
        else:
            messages.error(request, 'Please provide a comment.')
    return redirect('blog_detail', slug=slug)

@login_required
def blog_like(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    return redirect('blog_detail', slug=slug)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'main/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'main/blog_form.html'
    success_url = reverse_lazy('blog_list')

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author or self.request.user.is_staff

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blog_list')
    template_name = 'main/blog_confirm_delete.html'

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author or self.request.user.is_staff
