from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Destination, Package, Testimonial, Booking, Contact, PackageImage, Review, UserProfile, Safari, TourCategory, Blog, BlogComment
from .forms import BookingForm, BlogForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def home(request):
    featured_destinations = Destination.objects.filter(featured=True)[:3]
    featured_packages = Package.objects.filter(featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    return render(request, 'main/index.html', {
        'featured_destinations': featured_destinations,
        'featured_packages': featured_packages,
        'testimonials': testimonials
    })

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    packages = Package.objects.filter(destination=destination)
    return render(request, 'main/destination_detail.html', {
        'destination': destination,
        'packages': packages
    })

def package_detail(request, slug):
    package = get_object_or_404(Package, slug=slug)
    related_packages = Package.objects.filter(destination=package.destination).exclude(id=package.id)[:3]
    return render(request, 'main/package_detail.html', {
        'package': package,
        'related_packages': related_packages,
        'today': timezone.now().date()
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
    packages = Package.objects.all()
    tour_type = request.GET.get('tour_type')
    featured = request.GET.get('featured')
    price_range = request.GET.get('price_range')

    if tour_type:
        packages = packages.filter(tour_type=tour_type)
    if featured:
        packages = packages.filter(featured=True)
    if price_range:
        if price_range == 'budget':
            packages = packages.filter(price__lte=300)
        elif price_range == 'mid':
            packages = packages.filter(price__gt=300, price__lte=600)
        elif price_range == 'luxury':
            packages = packages.filter(price__gt=600)

    return render(request, 'main/packages.html', {
        'packages': packages
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
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            package=package,
            travel_date=request.POST.get('travel_date'),
            number_of_people=request.POST.get('number_of_people')
        )
        messages.success(request, 'Your booking has been received. We will contact you shortly!')
        return redirect('book')
    
    packages = Package.objects.all()
    return render(request, 'main/book.html', {
        'packages': packages
    })

@login_required
def booking_create(request):
    if request.method == 'POST':
        package = get_object_or_404(Package, id=request.POST.get('package'))
        form = BookingForm(request.POST, package=package)
        
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.total_price = package.price * booking.number_of_people
                booking.save()
                
                messages.success(request, 'Your booking has been created successfully!')
                return redirect('booking_detail', id=booking.id)
            except Exception as e:
                messages.error(request, 'Sorry, there was an error creating your booking. Please try again.')
                return redirect('package_detail', slug=package.slug)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('package_detail', slug=package.slug)
    
    return redirect('home')

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
