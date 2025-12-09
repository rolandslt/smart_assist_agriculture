from django.shortcuts import render
from .models import Farmer, Field, Crop , PlantingCalendar, RouteSafety , Weather, Language
from django.views import generic
# Create your views here.



#------------------
# Farmer Views
#------------------
class FarmerListView(generic.ListView):
    model= Farmer
    context_object_name = 'Farmer_list' # name for the list as a template variable
    template_name = 'farmers/farmer_list.html'

class FarmerDetailView(generic.DetailView):
    model = Farmer



#------------------
#Crop Views
#------------------

class CropListView(generic.ListView):
    model = Crop
    context_object_name = 'Crop_list'
    template_name = 'crops/crop_list.html'

class CropDetailView(generic.DetailView):
    model = Crop 



#------------------
# Fields Views
#------------------

class FieldListView(generic.ListView):
    model = Field
    context_object_name = 'Field_list'
    template_name = 'fields/field_list.html'

class FieldDetailView(generic.DetailView):
    model = Field


#------------------
# Planting Calendar Views
#------------------

class PlantingCalendarListView(generic.ListView):
    model = PlantingCalendar
    context_object_name = '_list'
    template_name = '/_list.html'

class PlantingCalendarDetailView(generic.DetailView):
    model = PlantingCalendar


#------------------
# Weather Record Views
#------------------

class WeatherDetailView(generic.DetailView):
    model = Weather
    context_object_name = 'Weather_detail'
    template_name = 'Weather/weather_detail.html'


#------------------
# Route Safety Record Views
#------------------

class RouteSafetyListView(generic.ListView):
    model = RouteSafety
    context_object_name = 'RouteSafety_list'
    template_name = 'RouteSafety/RouteSafety_list.html'


class  RouteSafetyDetailView(generic.DetailView):
    model =  RouteSafety
