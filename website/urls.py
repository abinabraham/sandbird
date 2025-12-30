from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('tour-package/', views.tour_package, name='tour_package'),
    path('tour-package/<slug:slug>/', views.tour_package_detail, name='tour_package_detail'),
    path('our-fleet/', views.our_fleet, name='our_fleet'),
    path('contact/', views.contact, name='contact'),
    path('prefs/', views.set_prefs, name='set_prefs'),
]
