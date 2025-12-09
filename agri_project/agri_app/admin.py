from django.contrib import admin
from .models import Farmer, Field, Weather, Crop, PlantingCalendar, RouteSafety, Language
# Register your models here.

#--------------------------
# Custom actions
#--------------------------
def mark_active(modeladmin, request, queryset):
    queryset.update(is_active=True)
mark_active.short_description = "Mark selected as active"

def mark_harvested(modeladmin, request, queryset):
    queryset.update(status='harvested')
mark_harvested.short_description = "Mark selected crops as harvested "

#--------------------------
# Farmer Admin
#--------------------------
@admin.register(Farmer)
class FArmerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'date_joined')
    search_fields = ('username', 'email', 'phone_number',)
    list_filter = ('date_joined',)
    actions = [mark_active]
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = 'date_joined'


# -----------------------
# Crop Admin
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
# Field Admin
# -----------------------
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name','farmer', 'location', 'size_in_hectares','soil_type')
    search_fields = ('name', 'location', 'soil_type', 'farmer',)
    actions = [mark_active]
    list_filter = ('soil_type',)
    actions_on_top = True
    actions_on_bottom = True
    actions_selection_counter = True


# -----------------------
# Weather Record Admin
# -----------------------
@admin.register(Weather)
class WEatherAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'temperature', 'humidity', 'rainfall', 'get_field')
    search_fields = ('location', 'date', 'temperature', 'humidity',)

    def get_field(self, obj):
        return obj.field.name if obj.field else '-'
    get_field.short_description = 'Field'

    
# -----------------------
# Planting Calendar Admin
# -----------------------
@admin.register(PlantingCalendar)
class PlantingCalendarAdmin(admin.ModelAdmin):
    list_display = ('crop', 'field', 'planting_date', 'harvest_date')
    search_fields = ('crop',)
    list_filter = ('planting_date',)
    date_hierarchy = 'planting_date'

# -----------------------
# Route Safety Admin
# -----------------------
@admin.register(RouteSafety)
class RouteSafetyAdmin(admin.ModelAdmin):
    list_display = ('route_name' , 'start_point', 'end_point', 'is_safe')
    search_fields = ('is_safe',)
    list_filter = ('is_safe',)

# -----------------------
# Register  Language with  Admin
# -----------------------
admin.site.register(Language)