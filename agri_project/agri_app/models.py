from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import AbstractUser
# Create your models here.

#------------------------
# Farmer and User
#------------------------
class Farmer(AbstractUser):
    email = models.EmailField(
        'email address', # verbose name for the admin site
        unique=True,     # <--- THIS IS THE CRUCIAL FIX
    )
    farm_name = models.CharField(
        max_length=150,
        unique=False,
        )
    phone_number = models.CharField(
        max_length=20,
        null=True, 
        blank=True)
    city_or_region = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            pass

     # --- CRUCIAL CONFIGURATION ---
    # The username field is required by AbstractUser. If you want to log in with email:
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] # Ensure username is still prompted during superuser creation

    class Meta:
        verbose_name= 'Farmer'
        verbose_name_plural='Farmers'

    def __str__(self):
        return self.username or self.email
    
#-------------------------------
# Field (farm plot)
#-------------------------------
class Field(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    size_in_hectares = models.FloatField()
    soil_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.farmer.username})"
    
#-------------------
# Crop
#-------------------
class Crop(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)  # e.g., vegetable, grain
    fields = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="crops")
    
    STATUS_CHOICES= [
        ('p', 'Planted'),           # Crop has been planted
        ('g', 'Growing'),           # Crop is still growing
        ('r', 'Ready for harvest'), # Crop is ready to be harvested
        ('h', 'Harvested'),         # Crop has been harvested
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default='p')
    
    planted_on = models.DateField(default=date.today)
    expected_harvest = models.DateField(null=True, blank=True)
    def __str__(self):
        return  f"{self.name} ({self.status})"

#-------------------------
# Planting Calendar
#-------------------------
class PlantingCalendar(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="calendar_entries", null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="calendar_entries", null=True, blank=True)
    planting_date = models.DateField()
    harvest_date = models.DateField()
    notes = models.TextField(blank=True)


    def __str__(self):
        target = self.crop.name if self.crop else self.field.name
        return f"Planting: {target} ({self.planting_date})"
    
#----------------------
# Weather  Record
#-----------------------
class Weather(models.Model):
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, blank=True)    
    location = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()

    def __str__(self):
        return f"Weather on {self.date} ({self.field.name})"
#------------------------
# Route Safety
#------------------------
class RouteSafety(models.Model):
    route_name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    is_safe = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route_name} - {'Safe' if self.is_safe else 'Unsafe'}"

#---------------------
# Language    
#---------------------
class Language(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

    
