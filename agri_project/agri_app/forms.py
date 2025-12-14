from django.contrib.auth.forms import UserCreationForm
from .models import Farmer ,Field , Crop, Activity, SecureRoute, WeatherRecord
from django import forms


#----------------
# Create Farmer 
#----------------
class FarmerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Farmer # <-- Crucial: Link the form to the custom model
        # fields must list all custom fields AND the fields you want to use
        fields = ('username', 'farm_name','email', 'phone_number','password')

class FarmerUpdateFrom(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['username', 'farm_name','email', 'phone_number','password', 'city_or_region']
#-------------------
# Create Field
#-------------------
class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'location', 'size_in_hectares', 'soil_type']

    # Add Tailwind CSS classes to the widgets for basic styling
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500', 
                'placeholder': 'e.g., North Acre, Valley Plot'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full  bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Near Main Road'
            }),
            'size_in_hectares': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., 5.5'
            }),
            'soil_type': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Clay, Loam, Sandy'
            }),
        }

#-------------------
# Create Crop
#-------------------
class CropForm(forms.ModelForm):
    def  __int__(self, *args, **kwargs):
        self.farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        if self.farmer:
            self.fields['fields'].queryset = Field.objects.filter(Farmer=self.farmer)
    class Meta:
        model = Crop
        fields = ['fields', 'name', 'description', 'category', 'planted_on', 'expected_harvest', 'status']

    # Add Tailwind CSS classes to the widgets for basic styling
        widgets = {
            'fields': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500'
            }),
            'name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500', 
                'placeholder': 'e.g., North Acre, Valley Plot'
            }),
            'description': forms.TextInput(attrs={
                'class': 'mt-1 block w-full  bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Near Main Road'
            }),
            'category': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., 5.5'
            }),
            'planted_on': forms.DateInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Clay, Loam, Sandy'
            }),
            'expected_harvest': forms.DateInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Clay, Loam, Sandy'
            }),

            'status': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Clay, Loam, Sandy'
            }),
        }

class ActivityFrom(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'field', 'scheduled_date', 'status', 'estimated_harvest_date']

class WeatherRecordForm(forms.ModelForm):
    class Meta:
        model = WeatherRecord
        fields = [ 'farmer', 'recorded_at', 'location', 'temperature', 'humidity', 'rainfall']
    
class SecureRouteForm(forms.ModelForm):
    class Meta:
        model= SecureRoute
        fields = ['route_name' , 'farmer', 'security_status']