from django.contrib import admin
from .models import Farmer, Field, Weather, Crop, PlantingCalendar, RouteSafety, Language
# Register your models here.

@admin.register(Farmer)
class FArmerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'date_joined')
    search_fields = ('username', 'email', 'phone_number',)
    list_filter = ('date_joined',)


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'date_added')
    search_fields = ('name', 'category',)
    list_filter = ('date_added',)



@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name','farmer', 'location', 'size_in_hectares','soil_type')
    search_fields = ('name', 'location', 'soil_type', 'farmer',)


@admin.register(Weather)
class WEatherAdmin(admin.ModelAdmin):
    list_display = ('date', 'location', 'temperature', 'humidity', 'rainfall', 'get_field')
    search_fields = ('location', 'date', 'temperature', 'humidity',)

    def get_field(self, obj):
        return obj.field.name if obj.field else '-'
    get_field.short_description = 'Field'

    

@admin.register(PlantingCalendar)
class PlantingCalendarAdmin(admin.ModelAdmin):
    list_display = ('crop', 'field', 'planting_date', 'harvest_date')
    search_fields = ('crop',)

@admin.register(RouteSafety)
class RouteSafetyAdmin(admin.ModelAdmin):
    list_display = ('route_name' , 'start_point', 'end_point', 'is_safe')
    search_fields = ('is_safe',)
    list_filter = ('is_safe',)

admin.site.register(Language)