from django.contrib.auth.forms import UserCreationForm
from .models import Farmer ,Field 
from django import forms


#----------------
# Create Farmer 
#----------------
class FarmerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Farmer # <-- Crucial: Link the form to the custom model
        # fields must list all custom fields AND the fields you want to use
        fields = ('username', 'farm_name','email', 'phone_number','password')


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