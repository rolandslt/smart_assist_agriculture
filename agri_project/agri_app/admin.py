from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Farmer, Crop, Field, Activity, WeatherRecord, SecureRoute, Review, Post, Comment


# --------------------------
# Custom actions
# --------------------------
# Action for Farmer/Field (Is Active)
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
mark_active.short_description = _("Mark selected as active")

# Action for Crop (Harvested) - Status must match your Crop model's status field.
def mark_harvested(modeladmin, request, queryset):
    # Assuming 'harvested' is a valid status choice in your Crop model
    queryset.update(status='harvested') 
mark_harvested.short_description = _("Mark selected crops as harvested")

# Action for Activity (Completed)
def mark_completed(modeladmin, request, queryset):
    # 'completed' is a valid status from the Activity model's choices
    queryset.update(status='completed')
mark_completed.short_description = _("Mark selected activities as completed")


#--------------------------
# Farmer Admin (No change needed)
#--------------------------
@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('farm_name', 'email', 'phone_number', 'date_joined')
    search_fields = ('farm_name', 'email', 'phone_number',)
    list_filter = ('date_joined',)
    actions = [mark_active]
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'date_joined'


# -----------------------
# Crop Admin (Using the existing mark_harvested action)
# -----------------------
@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','status', 'category','planted_on', 'expected_harvest')
    search_fields = ('name', 'category','status',)
    list_filter = ('status',)
    actions = [mark_harvested]
    actions_on_top = True
    actions_on_bottom = True
    

# -----------------------
# Field Admin (No change needed)
# -----------------------
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    # Added 'farmer' to list_display for better context
    list_display = ('name','farmer', 'location', 'size_in_hectares','soil_type')
    search_fields = ('name', 'location', 'soil_type', 'farmer',) # Use __username for FK lookup
    actions = [mark_active]
    list_filter = ('soil_type',)
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True


# -----------------------
# Activity Admin (New Name: PlantingCalendar -> Activity)
# -----------------------
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    # Updated fields: added farmer, status, used scheduled_date, estimated_harvest_date
    list_display = ('title', 'farmer', 'field', 'scheduled_date', 'status', 'estimated_harvest_date')
    search_fields = ('title', 'crop', 'field')
    list_filter = ('status', 'scheduled_date')
    date_hierarchy = 'scheduled_date' # Changed from planting_date
    actions = [mark_completed] # New action for marking activity as done
    list_select_related = ['farmer', 'field', 'crop'] # Optimize for FK lookups


# -----------------------
# Weather Record Admin (New Name: Weather -> WeatherRecord)
# -----------------------
@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    # Updated fields: added 'owner', renamed 'date' to 'recorded_at'
    list_display = ('farmer', 'recorded_at', 'location', 'temperature', 'humidity', 'rainfall', 'get_field')
    search_fields = ('location', 'recorded_at', 'temperature', 'humidity', 'farmer')

    def get_field(self, obj):
        # The relationship is now to 'field' as defined in the model
        return obj.field.name if obj.field else '-'
    get_field.short_description = 'Field'


# -----------------------
# Secure Route Admin (New Name: RouteSafety -> SecureRoute)
# -----------------------
@admin.register(SecureRoute)
class SecureRouteAdmin(admin.ModelAdmin):
    # Updated fields: added 'owner', using 'security_status', removed 'start_point'/'end_point'
    list_display = ('route_name' , 'farmer', 'security_status', 'last_updated')
    search_fields = ('route_name', 'risk_notes', 'farmer')
    list_filter = ('security_status',) # Filtering by status is more informative than by safety boolean
    # The map data (route_path_geojson) is too large to display here

    list_select_related = ['farmer'] # Optimize for owner lookup

# -----------------------
# Review , Post and Comment 
# -----------------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('content',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at') 
    search_fields = ('title', 'content')            
    list_filter = ('created_at', 'author')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ('content',)