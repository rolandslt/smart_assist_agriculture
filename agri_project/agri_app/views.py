from django.shortcuts import render
from .models import Farmer, Field, Crop , Activity, WeatherRecord, SecureRoute
from django.views import generic
from datetime import datetime
from .forms import FarmerCreationForm 
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView , ListView , UpdateView, DeleteView, TemplateView
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

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Farmer
    template_name = 'accounts/profile.html'
    context_object_name = 'farmer_profile'

    # Override get_object to fetch the currently logged-in user
    def get_object(self):
        return self.request.user
    
class FarmerProfileView(LoginRequiredMixin, TemplateView):
    model = Farmer
    template_name = 'profiles/farmer_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Manually set the object we want in the context
        context['farmer_profile'] = self.request.user 
        return context
    
class FarmerUpdateView(LoginRequiredMixin, UpdateView):
    model = Farmer
    template_name = 'profiles/farmer_form.html'
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'farm_name',
        'city_or_region',
        
    ]
    success_url = reverse_lazy('farmer_profile')
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        """Redirects to the profile detail page after a successful update."""
        return reverse_lazy('farmer_profile')


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
        return Field.objects.filter(farmer=self.request.user)

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


#------------------
#Crop Views
#------------------

class CropListView(LoginRequiredMixin, ListView):
    model = Crop
    context_object_name = 'crops'
    template_name = 'crops/crop_list.html'

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user).order_by('status', 'expected_harvest')
class CropDetailView(LoginRequiredMixin, DetailView):
    model = Crop 
    context_object_name = 'crop'
    template_name = 'crops/crop_detail.html'

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)

class CropCreateView(LoginRequiredMixin, CreateView):
    model = Crop
    template_name = 'crops/crop_form.html'
    fields = ['fields', 'name', 'description', 'category','planted_on', 'expected_harvest','status']
    success_url = reverse_lazy('crop_list')

    # Pass the current farmer to the form for queryset filtering (Step 2)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['farmer'] = self.request.user
        return kwargs

class CropUpdateView(LoginRequiredMixin, UpdateView):
    model = Crop
    template_name = 'crops/crop_form.html'
    fields = ['fields', 'name', 'description', 'category','planted_on', 'expected_harvest','status']
    success_url = reverse_lazy('crop_list')
    
    # Pass the current farmer to the form for queryset filtering (Step 2)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['farmer'] = self.request.user
        return kwargs
    
    # Ensure user can only update their own crop
    def get_queryset(self):
        return Field.objects.filter(fields__farmer=self.request.user)

class CropDeleteView(LoginRequiredMixin, DeleteView):
    model = Crop
    context_object_name = 'crop'
    template_name = 'crops/crop_delete_confirm.html'
    success_url = reverse_lazy('crop_list')

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)


#------------------
# Planting Calendar Views
#------------------

class ActivityListView(LoginRequiredMixin , ListView):
    model = Activity
    context_object_name = 'activities'
    template_name = 'activities/activity_list.html'

    def get_queryset(self):
        user=self.request.user
        queryset = Activity.objects.filter(farmer=user)
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('scheduled_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current filter back to the template
        context['current_status'] = self.request.GET.get('status', 'all')
        context['status_choices'] = Activity.STATUS_CHOICES 
        return context
    
class ActivityDetailView(generic.DetailView):
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/activity_detail.html'

    def get_queryset(self):
        return Activity.objects.filter(farmer=self.request.user)
    
class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    fields = ['title', 'field', 'scheduled_date', 'status', 'estimated_harvest_date']
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activity_list')

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the Field queryset to only include fields belonging to the current farmer
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        return form


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    fields = ['title', 'field', 'scheduled_date', 'status', 'estimated_harvest_date']
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activity_list')

    def get_queryset(self):
        return Activity.objects.filter(farmer=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        return form
    

class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/activity_delete_confirm.html'
    success_url = reverse_lazy('activity_list')

    def get_queryset(self):
        return Activity.objects.filter(farmer=self.request.user)   


#-----------------------------
# wWeather view Record
#------------------------------
class WeatherRecordListView(LoginRequiredMixin, ListView):
    model = WeatherRecord
    context_object_name = 'weather_list'
    template_name = 'weather/weather_list.html'
    paginate_by = 25
    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)

class WeatherRecordDetailView(LoginRequiredMixin, DetailView):
    model = WeatherRecord
    context_object_name = 'weather_detail'
    template_name = 'weather/weather_detail.html'

    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)
    
class WeatherRecordCreateView(LoginRequiredMixin, CreateView):
    model = WeatherRecord
    template_name = 'weather/weather_from.html'
    fields = ['recorded_at', 'location', 'temperature', 'humidity', 'rainfall']
    success_url = reverse_lazy('weather_list')

    def from_valid(self, form):
        form.instance.farmer = self.request.User
        return super().from_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        return form
    
class WeatherRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = WeatherRecord
    template_name = 'weather/weather_from.html'
    fields = ['recorded_at', 'location', 'temperature', 'humidity', 'rainfall']
    success_url = reverse_lazy('weather_list')

    def from_valid(self, form):
        form.instance.farmer = self.request.User
        return super().from_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        return form
    
    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)
    

class WeatherRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = WeatherRecord
    context_object_name = 'weather_delete'
    template_name = 'weathers/weather_delete_confirm.html'
    success_url = 'weather_list'
    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)
    
#------------------
# Route Safety Record Views
#------------------

class SecureRouteListView(LoginRequiredMixin, ListView):
    model = SecureRoute
    context_object_name='secure_route_list'
    template_name = 'routes/secure_route_list.html'

    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)
class SecureRouteDetailView(LoginRequiredMixin, DetailView):
    model = SecureRoute
    context_object_name='secure_route_detail'
    template_name = 'routes/secure_route_detail.html'


    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)
    
class SecureRouteCreateView(LoginRequiredMixin, CreateView):
    model = SecureRoute
    template_name = 'routes/secure_route_form.html'
    success_url = reverse_lazy('secure_route_list')
    fields = ['route_name', 'route_path_geojson', 'security_status', 'risk_notes']

    def form_valid(self, form):
        form.instance.farmer = self.request.user 
        return super().form_valid(form)
        
class SecureRouteUpdateView(LoginRequiredMixin, UpdateView):
    model = SecureRoute
    name='secure_route_update'
    template_name = 'routes/secure_route_form.html'
    success_url = reverse_lazy('secure_route_list')
    fields = ['route_name', 'route_path_geojson', 'security_status', 'risk_notes']

    def form_valid(self, form):
        form.instance.farmer = self.request.user 
        return super().form_valid(form)
    
    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)

class SecureRouteDeleteView(LoginRequiredMixin, DeleteView):
    model = SecureRoute
    context_object_name = 'secure_route_delete'
    template_name = 'routes/secure_route_delete_confirm.html'
    success_url = reverse_lazy('secure_route_list')

    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user) 
