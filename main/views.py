from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Destination, Package, Testimonial, Booking

def home(request):
    destinations = Destination.objects.all()[:3]
    packages = Package.objects.all()[:3]
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'main/index.html', {
        'destinations': destinations,
        'packages': packages,
        'testimonials': testimonials
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
    return render(request, 'main/packages.html', {
        'packages': packages
    })

def blog(request):
    return render(request, 'main/blog.html')

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
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
