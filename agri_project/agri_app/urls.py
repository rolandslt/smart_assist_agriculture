from django.urls import path
from . import views  # import your app views

urlpatterns = [
    # Farmer urls
    path('farmer/',views.FarmerListView.as_view(), name='farmers'),
    path('farmer/<int:pk>', views.FarmerDetailView.as_view(), name='farmer-detail'),

    # Crop urls
    path('crop/', views.CropListView.as_view(), name='crops'),
    path('crop/<int:pk>', views.CropDetailView.as_view(), name='crop-detail'),

    # Field urls
    path('crop/', views.FieldListView.as_view(), name='Fields'),
    path('crop/<int:pk>', views.FieldDetailView.as_view(), name='field-detail'),

    # Planting Calendar urls
    path('PlantingCalendar/', views.PlantingCalendarListView.as_view(), name='planting-calendar'),
    path('crop/<int:pk>', views.PlantingCalendarDetailView.as_view(), name='planting-calendar-detail'),

    # Weather Record urls
    path('weather/<int:pk>', views.WeatherDetailView.as_view(), name='weather-detail'),



    # Route Safety urls
    path('RouteSafety/', views.RouteSafetyListView.as_view(), name='route-safety'),
    path('RouteSafety/<int:pk>', views.RouteSafetyDetailView.as_view(), name='route-safety-detail'),
]

