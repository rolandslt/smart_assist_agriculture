from rest_framework import serializers
from .models import Farmer, Crop, Field, WeatherRecord, Activity, SecureRoute, Review, Post, Comment
from django.contrib.auth import get_user_model
Farmer = get_user_model() 


#----------------------
# Farmer Serializers
#-----------------------
class FarmerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = [
            'id', 
            'username', 
            'farm_name', 
            'city_or_region'
        ]


class FarmerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = [
            'id', 
            'username', 
            'first_name', 
            'last_name',
            'email', 
            'farm_name', 
            'phone_number', 
            'city_or_region' 
            
        ]
        read_only_fields = fields

class FarmerCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Farmer
        fields = [
            'username', 
            'email', 
            'farm_name', 
            'phone_number', 
            'password'
        ]

    def create(self, validated_data):
        # Use create_user to handle password hashing automatically
        return Farmer.objects.create_user(**validated_data)

class FarmerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'phone_number', 
            'farm_name', 
            'city_or_region'
        ]
#----------------------
# Field Serializers
#-----------------------
class FieldListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = [
            'id', 
            'name', 
            'size_in_hectares', 
            'soil_type'
        ]


class FieldDetailSerializer(serializers.ModelSerializer):
    farmer = serializers.ReadOnlyField(source='farmer.username')
    class Meta:
        model = Field
        fields = [
            'id', 
            'name', 
            'size_in_hectares', 
            'soil_type', 
            'farmer'     
        ]
        

class FieldCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = [
            'name', 
            'size_in_hectares', 
            'soil_type'
        ]

class FieldUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = [
            'name', 
            'size_in_hectares', 
            'soil_type'
        ]

#----------------------
# Crop Serializers
#-----------------------
class CropListSerializer(serializers.ModelSerializer):
    field_name = serializers.ReadOnlyField(source='fields.name')
    class Meta:
        model = Crop
        fields = [
            'id', 
            'name', 
            'status', 
            'expected_harvest', 
            'field_name'

        ]

class CropDetailSerializer(serializers.ModelSerializer):
    fields = serializers.ReadOnlyField(source='fields.name')
    class Meta:
        model = Crop
        fields = '__all__'

class CropCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields =[
            'name', 
            'description', 
            'category', 
            'fields', 
            'planted_on', 
            'expected_harvest', 
            'status'
        ]

    def validate_fields(self, value):
            """
            Security Check: Ensure the field being assigned belongs 
            to the farmer making the request.
            """
            user = self.context['request'].user
            if value.farmer != user:
                raise serializers.ValidationError("You cannot add a crop to a field you do not own.")
            return value
            

#---------------------------------
# Planting calendar Serializers
#--------------------------------
class ActivityListSerializer(serializers.ModelSerializer):
    field_name = serializers.ReadOnlyField(source='field.name')
    class Meta:
        model = Activity
        fields = [
            'id', 
            'title', 
            'field_name', 
            'scheduled_date', 
            'status'

        ]

class ActivityDetailSerializer(serializers.ModelSerializer):
    farmer_name = serializers.ReadOnlyField(source='farmer.username')
    field_name = serializers.ReadOnlyField(source='field.name')
    crop_name = serializers.ReadOnlyField(source='crop.name')
    class Meta:
        model = Activity
        fields ='__all__'

class ActivityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'title', 
            'field', 
            'scheduled_date', 
            'status', 
            'estimated_harvest_date', 
            'crop', 
            'description'

        ]
        def validate(self, data):
            """
            Cross-field validation: Ensure both Field and Crop belong to the user.
            """
            user = self.context['request'].user
        
            # Check Field ownership
            if data.get('field') and data['field'].farmer != user:
                raise serializers.ValidationError({"field": "This field does not belong to you."})
            
            # Check Crop ownership (assuming Crop relates to Field, which relates to Farmer)
            if data.get('crop') and data['crop'].field.farmer != user:
                raise serializers.ValidationError({"crop": "This crop does not belong to your fields."})
            
            return data



#----------------------
# Weather Serializers
#-----------------------
class WeatherRecordListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields =[
            'id', 
            'recorded_at', 
            'location', 
            'temperature', 
            'humidity', 
            'rainfall'

        ]

class WeatherRecordDetailSerializer(serializers.ModelSerializer):
    field_name = serializers.ReadOnlyField(source='field.name')
    farmer_name = serializers.ReadOnlyField(source='farmer.username')
    class Meta:
        model = WeatherRecord
        fields ='__all__'
class WeatherRecordCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecord
        fields =[
            'recorded_at', 
            'field', 
            'location', 
            'temperature', 
            'humidity', 
            'rainfall', 
            'wind_speed', 
            'source'
        ]

    def validate_field(self, value):
        # Ensure the field belongs to the person logging the weather
        user = self.context['request'].user
        if value.farmer != user:
            raise serializers.ValidationError("You cannot record weather for a field you do not own.")
        return value
        

#----------------------
# Route Safety Serializers
#-----------------------
class SecureRouteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureRoute
        fields =[
            'id', 
            'route_name', 
            'security_status'
        ]
class SecureRouteDetailSerializer(serializers.ModelSerializer):
    farmer_name= serializers.ReadOnlyField(source='farmer.username')
    class Meta:
        model = SecureRoute
        fields ='__all__'

class SecureRouteCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureRoute
        fields =[
            'route_name', 
            'route_path_geojson', 
            'security_status', 
            'risk_notes'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    farmer_name = serializers.ReadOnlyField(source='farmer.username')
    class Meta:
        model = Review
        fields = ['id', 'farmer', 'farmer_name', 'content', 'rating', 'created_at']
        read_only_fields = ['farmer', 'created_at']
        
class CommentSerializer(serializers.ModelSerializer):
    farmer_name = serializers.ReadOnlyField(source='farmer.username')

    class Meta:
        model = Comment
        fields = ['id', 'farmer_name', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    # This matches the 'comment_set' to show comments inside the post object
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'comments']