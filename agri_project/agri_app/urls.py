from django.urls import path, include
from . import views  # import your app views
from django.views.generic import TemplateView
urlpatterns = [
    # Home page
    path('',views.index, name='home'),

    # Farmer urls
    path('farmer/',views.FarmerListView.as_view(), name='farmer_list'),
    path('farmer/<int:pk>', views.FarmerDetailView.as_view(), name='farmer_detail'),

    # Crop urls
    path('crop/', views.CropListView.as_view(), name='crop_list'),
    path('crop/<int:pk>', views.CropDetailView.as_view(), name='crop_detail'),

    # Field urls
    path('fields/', views.FieldListView.as_view(), name='field_list'),
    path('fields/<int:pk>', views.FieldDetailView.as_view(), name='field_detail'),
    path('fields/add/', views.FieldCreateView.as_view(), name='field_create'),
    path('fields/<int:pk>/edit', views.FieldUpdateView.as_view(), name='field_update'),
    path('fields/<int:pk>/delete/', views.FieldDeleteView.as_view(), name='field_delete'),



    # Planting Calendar urls
    path('PlantingCalendar/', views.PlantingCalendarListView.as_view(), name='calendar_list'),
    path('crop/<int:pk>', views.PlantingCalendarDetailView.as_view(), name='planting_calendar_detail'),
    
    # Weather Record urls
    path('weather,', views.WeatherListView.as_view(), name='weather_list'),
    path('weather/<int:pk>', views.WeatherDetailView.as_view(), name='weather_detail'),



    # Route Safety urls
    path('RouteSafety/', views.RouteSafetyListView.as_view(), name='route_safety'),
    path('RouteSafety/<int:pk>', views.RouteSafetyDetailView.as_view(), name='route_safety_detail'),

    # Registration, Login, Logout Views
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',views.ProfileDetail.as_view(template_name='accounts/profile.html'),name='profile'),
    path("registration/", views.SignUpView.as_view(), name='sign_up'),
]

