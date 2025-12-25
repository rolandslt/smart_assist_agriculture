from rest_framework import viewsets, permissions, generics
from .models import Farmer, Field, Crop, WeatherRecord, SecureRoute, Activity
from .serializers import (
    FarmerListSerializer, FarmerDetailSerializer, 
    FarmerCreateSerializer, FarmerUpdateSerializer,
    FieldListSerializer, FieldDetailSerializer,
    FieldCreateSerializer, CropListSerializer,
    CropDetailSerializer, CropCreateUpdateSerializer,
    ActivityListSerializer, ActivityDetailSerializer,
    ActivityCreateUpdateSerializer, WeatherRecordListSerializer,
    WeatherRecordDetailSerializer, WeatherRecordCreateUpdateSerializer,
    SecureRouteListSerializer, SecureRouteDetailSerializer, 
    SecureRouteCreateUpdateSerializer
)

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return FarmerListSerializer
        if self.action == 'retrieve':
            return FarmerDetailSerializer
        if self.action == 'create':
            return FarmerCreateSerializer
        if self.action in ['update', 'partial_update']:
            return FarmerUpdateSerializer
        return FarmerUpdateSerializer
            
class FieldViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Field.objects.filter(farmer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return FieldListSerializer
        if self.action == 'retrieve':
            return FieldDetailSerializer
        return FieldCreateSerializer
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)    
        
    
class CropViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CropListSerializer
        if self.action == 'retrieve':
            return CropDetailSerializer
        return CropCreateUpdateSerializer
    
class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(field__farmer=self.request.user).order_by('scheduled_date')

    def get_serializer_class(self):
        if self.action == 'list':
            return ActivityListSerializer
        if self.action == 'retrieve':
            return ActivityDetailSerializer
        return ActivityCreateUpdateSerializer
    
class WeatherRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user).order_by('-recorded_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return WeatherRecordListSerializer
        if self.action == 'retrieve':
            return WeatherRecordDetailSerializer
        return WeatherRecordCreateUpdateSerializer
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
class SecureRouteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return SecureRouteListSerializer
        if self.action == 'retrieve':
            return SecureRouteDetailSerializer
        return SecureRouteCreateUpdateSerializer
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)