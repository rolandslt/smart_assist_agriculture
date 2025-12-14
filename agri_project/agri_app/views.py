from django.shortcuts import render
from .models import Farmer, Field, Crop , PlantingCalendar, RouteSafety , Weather, Language
from django.views import generic
from datetime import datetime
from .forms import FarmerCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView , ListView , UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
Farmer = get_user_model() 
# Create your views here.

#----------------
# Home page 
#----------------
def index(request):
    context = {'word':'welcome home'}
    return render(request , 'index.html', context)

#------------------
# Farmer Sin in 
#------------------
class SignUpView(CreateView):
    model = Farmer
    from_class = FarmerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'
    fields = ('username', 'farm_name','email', 'phone_number', 'password')
#---------------
# Farmer Profile
#----------------
class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Farmer
    template_name = 'accounts/profile.html'
    context_object_name = 'farmer'

    # Override get_object to fetch the currently logged-in user
    def get_object(self):
        return self.request.user



#------------------
# Fields Views
#------------------

class FieldListView(LoginRequiredMixin, ListView):
    """
    Displays a list of all fields belonging to the current logged-in farmer.
    """
    model = Field
    context_object_name = 'fields'
    template_name = 'fields/field_list.html'

    def get_queryset(self):
        """
        Overrides the queryset to filter fields by the currently logged-in user.
        """
        return Field.objects.filter(Farmer=self.request.user)

class FieldDetailView(LoginRequiredMixin, DetailView):
    model = Field
    template_name = 'field_detail.html'
    context_object_name = 'field'

    
    
class FieldCreateView(LoginRequiredMixin, CreateView):
    model = Field
    template_name = 'fields/field_form.html'
    fields = ['name', 'size_in_hectares', 'soil_type']
    success_url = reverse_lazy('field_list')

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super().form_valid(form)

class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = Field
    template_name ='fields/field_form.html'
    fields = ['name', 'size_in_hectares', 'soil_type']
    success_url = reverse_lazy('field_list')


    def get_queryset(self):
        return Field.objects.filter(farmer=self.request.user)

class FieldDeleteView(LoginRequiredMixin, DeleteView):
    model = Field
    context_object_name = 'field'
    template_name = 'field_confirm_delete.html'
    success_url = reverse_lazy('field_list')

    def get_queryset(self):
        return Field.objects.filter(farmer=self.request.user)

























# Farmer Views
#------------------
class FarmerListView(generic.ListView):
    model= Farmer
    context_object_name = 'farmer_list' # name for the list as a template variable
    template_name = 'farmers/farmer_list.html'

class FarmerDetailView(generic.DetailView):
    model = Farmer



#------------------
#Crop Views
#------------------

class CropListView(generic.ListView):
    model = Crop
    context_object_name = 'crop_list'
    template_name = 'crops/crop_list.html'

class CropDetailView(generic.DetailView):
    model = Crop 



#------------------
# Fields Views
#------------------

class FieldListView(generic.ListView):
    model = Field
    context_object_name = 'field_list'
    template_name = 'fields/field_list.html'

class FieldDetailView(generic.DetailView):
    model = Field


#------------------
# Planting Calendar Views
#------------------

class PlantingCalendarListView(generic.ListView):
    model = PlantingCalendar
    context_object_name = '_list'
    template_name = 'PlantingCalendar/Planting_Calendar_list.html'

class PlantingCalendarDetailView(generic.DetailView):
    model = PlantingCalendar


#------------------
# Weather Record Views
#------------------

class WeatherListView(generic.ListView):
    model = Weather
    context_object_name = 'Weather_list'
    template_name = 'Weather/weather_list.html'

class WeatherDetailView(generic.DetailView):
    model = Weather

#------------------
# Route Safety Record Views
#------------------

class RouteSafetyListView(generic.ListView):
    model = RouteSafety
    context_object_name = 'RouteSafety_list'
    template_name = 'RouteSafety/RouteSafety_list.html'


class  RouteSafetyDetailView(generic.DetailView):
    model =  RouteSafety
