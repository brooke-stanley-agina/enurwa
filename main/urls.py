from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<slug:slug>/', views.destination_detail, name='destination_detail'),
    path('packages/', views.packages, name='packages'),
    path('package/<slug:slug>/', views.package_detail, name='package_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/comment/', views.blog_comment, name='blog_comment'),
    path('blog/<slug:slug>/like/', views.blog_like, name='blog_like'),
    path('contact/', views.contact, name='contact'),
    path('book/', views.book, name='book'),
    path('booking/create/', views.booking_create, name='booking_create'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('blog/new/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blog/<slug:slug>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<slug:slug>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
