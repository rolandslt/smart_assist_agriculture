from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

# Farmer and User
class Farmer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure at least one login method is provided
        if not self.email and not self.phone_number:
            raise ValidationError("Farmer must have either an email or a phone number")
    def __str__(self):
        return self.username
    

# Field (farm plot)
class Field(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="fields")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    size_in_hectares = models.FloatField()
    soil_type = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} ({self.farmer.username})"
    

# Crop
class Crop(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)  # e.g., vegetable, grain
    fields = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="crops")
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# Planting Calendar
class PlantingCalendar(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="calendar_entries", null=True, blank=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="calendar_entries", null=True, blank=True)
    planting_date = models.DateField()
    harvest_date = models.DateField()
    notes = models.TextField(blank=True)


    def __str__(self):
        target = self.crop.name if self.crop else self.field.name
        return f"Planting: {target} ({self.planting_date})"
    

# Weather   
class Weather(models.Model):
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, null=True, blank=True)    
    location = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()

    def __str__(self):
        return f"Weather on {self.date} ({self.field.name})"
    
# Route Safety
class RouteSafety(models.Model):
    route_name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    is_safe = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route_name} - {'Safe' if self.is_safe else 'Unsafe'}"
    
# Language    
class Language(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

    
