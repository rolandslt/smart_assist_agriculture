from rest_framework import viewsets, permissions, generics, filters
from .models import Farmer, Field, Crop, WeatherRecord, SecureRoute, Activity, Review, Post ,Comment
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
    SecureRouteCreateUpdateSerializer, ReviewSerializer, 
    PostSerializer
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.authentication import TokenAuthentication

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'farm_name', 'first_name', 'last_name','city_or_region']

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
    
    def get_permissions(self):
        if self.action == 'create':
            # This allows anyone to register without a token
            permission_classes = [permissions.AllowAny]
        else:
            # This requires a token for GET, PUT, PATCH, DELETE
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes] 

    def get_queryset(self):
        # The user is identified by the Token in the header
        user = self.request.user
        
        # If not logged in (e.g., during registration), return nothing
        if not user.is_authenticated:
            return Farmer.objects.none()
            
        # Filter the Farmer table so only the logged-in user's data is returned
        return Farmer.objects.filter(id=user.id)
         
class FieldViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['size_in_hectares', 'soil_type']

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
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category', 'status']

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return CropListSerializer
        if self.action == 'retrieve':
            return CropDetailSerializer
        return CropCreateUpdateSerializer
    
class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    authentication_classes = [TokenAuthentication]
   

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
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = [ 'location']

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
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['route_name', 'route_path_geojson', 'security_status', 'risk_notes']

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

class ReviewSetView(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-created_at')[:5]
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the 'farmer' to the logged-in user
        serializer.save(farmer=self.request.user)

class PostViewSet(viewsets.ModelViewSet):
    # Fetch latest 10 posts and their comments in one efficient query
    queryset = Post.objects.all().order_by('-created_at').prefetch_related('comment_set')[:10]
    serializer_class = PostSerializer