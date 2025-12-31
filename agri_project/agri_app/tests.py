from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Field, Crop, Activity, WeatherRecord, SecureRoute
import json
Farmer = get_user_model()

class AgriProjectFullTest(APITestCase):
    
    def setUp(self):
        # 1. Create Farmers
        self.farmer_a = Farmer.objects.create_user(
            username='farmer_a', email='a@test.com', password='password123'
        )
        self.farmer_b = Farmer.objects.create_user(
            username='farmer_b', email='b@test.com', password='password123'
        )
        
        # 2. Authenticate Farmer A
        response = self.client.post('/api-token-auth/', {
            'username': 'farmer_a', 'password': 'password123'
        })
        self.token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # 3. Create Fields
        self.field_a = Field.objects.create(name="Alpha", farmer=self.farmer_a, size_in_hectares=5)
        self.field_b = Field.objects.create(name="Beta", farmer=self.farmer_b, size_in_hectares=10)

    def test_farmer_list_visibility(self):
        url = reverse('farmer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_field_isolation(self):
        url = reverse('field-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1) # Only see Alpha

    def test_crop_creation_security(self):
        url = reverse('crop-list')
        data = {
            "name": "Theft Maize",
            "category": "Cereal", # Added missing field
            "fields": self.field_b.id, 
            "status": "planted"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You cannot add a crop to a field you do not own.", str(response.data))

    def test_activity_search(self):
        Activity.objects.create(
            title="Harvesting Task", 
            field=self.field_a, 
            farmer=self.farmer_a, # Added missing required field
            status="pending",
            scheduled_date="2025-12-30"
        )
        url = f"{reverse('activity-list')}?search=Harvest"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

    def test_weather_post_assignment(self):
        # Changed to lowercase 'weatherrecord'
        url = reverse('weather-record-list') 
        
        data = {
            "recorded_at": "2025-12-29T10:00:00Z",
            "field": self.field_a.id,
            "location": "North Farm",
            "temperature": 25.0,
            "humidity": 60.0,
            "rainfall": 0.0,  # <--- Add this
            "wind_speed": 5.0,
            
        }
        response = self.client.post(url, data, format='json')
        if response.status_code != 201:
            print(f"\nSECURE ROUTE ERROR: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_secure_route_creation(self):
        url = reverse('secure-route-list')
        geojson_data = {
        "type": "LineString", 
        "coordinates": [[0.0, 0.0], [1.0, 1.0]]
        }
        data = {
            "route_name": "Emergency Exit",
            "route_path_geojson": json.dumps(geojson_data),
            "security_status": "yellow",  # Ensure this matches your model choices
            "risk_notes": "No immediate threats detected."
        }
        
        response = self.client.post(url, data, format='json')
        
        # If it fails, this will print the EXACT error from the serializer
        if response.status_code != 201:
            print(f"\nSECURE ROUTE VALIDATION ERROR: {response.data}")
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)