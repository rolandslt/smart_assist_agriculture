from django.db import models

# Create your models here.
class Farmer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)


class Crop(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)  # e.g., vegetable, grain
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="crops")
    date_added = models.DateTimeField(auto_now_add=True)

class PlantingCalendar(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name="calendar_entries")
    planting_date = models.DateField()
    harvest_date = models.DateField()
    notes = models.TextField(blank=True)

class Weather(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, null=True, blank=True)  # optional
    location = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()

class RouteSafety(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name="routes")
    route_name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    is_safe = models.BooleanField(default=True)

class Language(models.Model):
    name = models.CharField(max_length=30, unique=False)
    