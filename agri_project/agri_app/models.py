from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.

#------------------------
# Farmer and User
#------------------------
class FarmerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValidationError('Farmers must have an email address')
        
        email = self.normalize_email(email)
        # Force security defaults for regular farmers
        extra_fields.setdefault('username', email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)


        # --- PERMISSION CONTROL START ---
        # You can trigger a logic here to auto-assign a 'Farmer' group
        # or set default row-level permissions
        # --- PERMISSION CONTROL END ---

        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Farmer(AbstractUser):
    email = models.EmailField(
        'email address', 
        unique=True,        
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
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    objects = FarmerManager()
    

    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            pass

     # --- CRUCIAL CONFIGURATION ---
    
    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['email'] # Ensure username is still prompted during superuser creation

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
        ('planted', 'Planted'),           # Crop has been planted
        ('growing', 'Growing'),           # Crop is still growing
        ('ready ', 'Ready for harvest'), # Crop is ready to be harvested
        ('harvested', 'Harvested'),         # Crop has been harvested
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=True,
        default='planted')
    
    planted_on = models.DateField(default=date.today)
    expected_harvest = models.DateField(null=True, blank=True)
    def __str__(self):
        return  f"{self.name} in {self.fields.name} ({self.status})"
    
    class Meta:
        ordering = ['-planted_on']

#-------------------------
# Planting Calendar
#-------------------------
class Activity(models.Model):
    """
    Represents a scheduled or completed farming activity/task (Planting, Fertilizing, etc.).
    """
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='activities', 
                               help_text=("The farmer/user who scheduled this activity."))
    crop = models.ForeignKey(Crop, on_delete=models.SET_NULL, related_name="activities", 
                             null=True, blank=True) 
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name="activities", 
                              null=True, blank=True) 

    title = models.CharField(max_length=255, 
                             help_text=("e.g., Planting, Fertilizing, Scouting, Harvesting"))
    description = models.TextField(blank=True, help_text=("Detailed notes on the task."))
    
    # Scheduled date for ANY task
    scheduled_date = models.DateField(help_text=("The date the activity is scheduled or completed."))
    
    # Optional field, useful if the activity is a planting task
    estimated_harvest_date = models.DateField(null=True, blank=True) 
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )

    def __str__(self):
        return f"{self.title}: {self.field.name if self.field else 'N/A'} ({self.scheduled_date})"

    class Meta:
        verbose_name = ("Scheduled Activity")
        verbose_name_plural = ("Scheduled Activities")
        ordering = ['scheduled_date']
#----------------------
# Weather  Record
#-----------------------
class WeatherRecord(models.Model): 
    """
    Stores historical or manually input weather data linked to a field.
    """
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='weather_records',
                              help_text=("The farmer who owns this weather record."))
    
    field = models.ForeignKey(Field, on_delete=models.SET_NULL, related_name='weather_records',
                              null=True, blank=True) 
    
    recorded_at = models.DateTimeField(default=timezone.now, 
                                       help_text=("Date and time the reading was taken.")) 
    
    location = models.CharField(max_length=100, blank=True, 
                                help_text=("City or specific GPS reference."))
    
    temperature = models.FloatField(help_text=("Temperature in °C."))
    
    humidity = models.FloatField(help_text=("Humidity percentage (0-100)."))
    
    rainfall = models.FloatField(help_text=("Rainfall/precipitation in millimeters."))
    
    wind_speed = models.FloatField(null=True, blank=True,
                                   help_text=("Wind speed in mph, km/h, or m/s"))

    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('api', 'Weather API'),
        ('sensor', 'IoT Sensor'),
    ]
    
    source = models.CharField(
        max_length=50, 
        choices=SOURCE_CHOICES, 
        default='manual',
        help_text=("Data source (e.g., manual, API, sensor).")
        )

    def __str__(self):
        return f"Weather for {self.field.name if self.field else 'N/A'} at {self.recorded_at.date()}"

    class Meta:
        verbose_name = ("Weather Record")
        verbose_name_plural = ("Weather Records")
        ordering = ['-recorded_at']
        unique_together = ('field', 'recorded_at')
#------------------------
# Route Safety
#------------------------
class SecureRoute(models.Model): 
    """
    Stores a defined route path and associated security data for transport safety.
    """
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='secure_routes',
                              help_text=("The user who created or last updated this route."))
    
    route_name = models.CharField(max_length=100, help_text=("A descriptive name for the route (e.g., 'Farm to Goma Market')."))
    
    
    route_path_geojson = models.TextField(
        help_text=("The geographical data (GeoJSON) defining the route path for map display.")
    )
    
    SECURITY_LEVELS = [
        ('green', 'Safe (Low Risk)'),
        ('yellow', 'Caution (Medium Risk)'),
        ('red', 'Unsafe (High Risk / Blocked)')
    ]
    security_status = models.CharField(
        max_length=10,
        choices=SECURITY_LEVELS,
        default='yellow', 
        help_text=("The assessed security level for the route.")
    )
    
    risk_notes = models.TextField(blank=True, 
                                  help_text=("Details on security threats or blockages."))
    
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.route_name} - {self.get_security_status_display()}"
        
    class Meta:
        verbose_name = ("Secure Transport Route")
        verbose_name_plural = ("Secure Transport Routes")
        ordering = ['-last_updated']

    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateField(auto_now_add=True)
    tags = TaggableManager(blank=True)

    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='comment')

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment')

    @property
    def total_likes(self):
        return self.likes.count()
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
   


    def __str__(self):
        return f'Comment by {self.author} on {self.post.title}'
    
class Review(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.farmer.username}"