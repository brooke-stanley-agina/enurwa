from django.conf import settings
from django.db.models import Avg
from .models import Booking, Package, UserProfile, Testimonial

def google_maps_api_key(request):
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }

def admin_stats(request):
    """
    Context processor to provide statistics for the admin dashboard
    """
    if not request.path.startswith('/admin/'):
        return {}

    try:
        booking_count = Booking.objects.filter(status='active').count()
        customer_count = UserProfile.objects.count()
        safari_count = Package.objects.filter(is_featured=True).count()
        rating_avg = Testimonial.objects.aggregate(Avg('rating'))['rating__avg']
        
        if rating_avg:
            rating_avg = round(rating_avg, 1)
        else:
            rating_avg = 0

        return {
            'booking_count': booking_count,
            'customer_count': customer_count,
            'safari_count': safari_count,
            'rating_avg': rating_avg,
        }
    except:
        return {
            'booking_count': 0,
            'customer_count': 0,
            'safari_count': 0,
            'rating_avg': 0,
        } 