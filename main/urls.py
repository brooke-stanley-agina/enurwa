from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('packages/', views.packages, name='packages'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('book/', views.book, name='book'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
