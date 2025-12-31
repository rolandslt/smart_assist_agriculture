from django.contrib.auth.forms import UserCreationForm
from .models import Farmer ,Field , Crop, Activity, SecureRoute, WeatherRecord, Comment, Post
from django import forms


#----------------
# Create Farmer 
#----------------
class FarmerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Farmer # <-- Crucial: Link the form to the custom model
        # fields must list all custom fields AND the fields you want to use
        fields = ( 'farm_name','username','email', 'phone_number')

class FarmerUpdateForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['profile_photo','username', 'farm_name','first_name','last_name','email', 'phone_number', 'city_or_region']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                }),
            'farm_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                }),
            'first_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                }),
            'email': forms.EmailInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500', 
                'placeholder': 'example@mail.com'}),
            'phone_number': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500', 
                'placeholder': '+243...'
                }),
            'city_or_region': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                }),
            'profile_photo': forms.FileInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
            }),
        }
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
            'description': forms.Textarea(attrs={
                'class': 'mt-1 block w-full  bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., High-yield variety, North section',
                'rows': 2
            }),
            'category': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Cereal, Legume'
            }),
            'planted_on': forms.DateInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'type': 'date'
            }),
            'expected_harvest': forms.DateInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'type': 'date'
            }),

            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Clay, Loam, Sandy'
            }),
        }
    def  __init__(self, *args, **kwargs):
        self.farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        if self.farmer:
            self.fields['fields'].queryset = Field.objects.filter(farmer=self.farmer)

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'field', 'crop','scheduled_date', 'status', 'estimated_harvest_date']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'placeholder': 'e.g., Planting, Fertilizing, Scouting, Harvesting'
            }),
            'field': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500'
            }),
            'crop': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500'
            }),
            'scheduled_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'type': 'date'  
            }),
            'status': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500'
            }),
            'estimated_harvest_date': forms.DateInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-green-500 focus:border-green-500',
                'type': 'date'
            }),
        }

    
class WeatherRecordForm(forms.ModelForm):
    class Meta:
        model = WeatherRecord
        fields = [ 'field', 'recorded_at', 'temperature', 'humidity', 'rainfall', 'source', 'wind_speed']
    
        

        widgets = {
            'field': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700'
                }),
            'recorded_at': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700',
                'type': 'datetime-local' 
            }),
            
            'temperature': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700', 
                'placeholder': '°C'
            }),
            'humidity': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700', 
                'placeholder': '%'
            }),
            'rainfall': forms.NumberInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700', 
                'placeholder': 'mm'
            }),
            'source': forms.Select(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700'
            }),
            'wind_speed' : forms.NumberInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700',
                'placeholder': 'mph'
            }),
        }
class SecureRouteForm(forms.ModelForm):
    class Meta:
        model= SecureRoute
        fields = ['route_name' , 'security_status', 'risk_notes', 'route_path_geojson']
        

        widgets = {
            'route_name': forms.TextInput(attrs={
                'class': 'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700',
                'placeholder': 'e.g., Main Access Road'
            }),
            
            'security_status': forms.Select(attrs={
                'class':'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700'
            }),
            'risk_notes': forms.Textarea(attrs={
                'class':'mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm p-2 focus:ring-1 focus:ring-green-500 focus:border-green-500 text-gray-700',
                'rows': 3
            }),
            'route_path_geojson': forms.HiddenInput(attrs={'id': 'id_route_path_geojson'}),
        }

    def  __init__(self, *args, **kwargs):
        self.farmer = kwargs.pop('farmer', None)
        super().__init__(*args, **kwargs)
        if self.farmer:
            self.fields['fields'].queryset = Field.objects.filter(farmer=self.farmer)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']