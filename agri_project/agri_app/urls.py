from django.urls import path, include
from . import views  # import your app views
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter 
from .api_views import FarmerViewSet , FieldViewSet, CropViewSet, ActivityViewSet, WeatherRecordViewSet, SecureRouteViewSet, ReviewSetView, PostViewSet

router =  SimpleRouter()
router.register(r'farmers', FarmerViewSet, basename='farmer'),
router.register(r'fields', FieldViewSet, basename='field'),
router.register(r'crops', CropViewSet, basename='crop'),
router.register(r'activities', ActivityViewSet, basename='activity'),
router.register(r'weather',WeatherRecordViewSet, basename='weather-record'),
router.register(r'secure-routes', SecureRouteViewSet, basename='secure-route'),
router.register(r'reviews', ReviewSetView, basename='review'),
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    # Home page
    path('',views.index, name='home'),
    path('submit_review/', views.SubmitReview, name='submit_review'),
    path('reviews/all/', views.AllReview, name='all_reviews'),

    # Crop urls
    path('crops/', views.CropListView.as_view(), name='crop_list'),
    path('crops/<int:pk>', views.CropDetailView.as_view(), name='crop_detail'),
    path('crops/<int:pk>', views.CropDetailView.as_view(), name='crop_detail'),
    path('crops/add/', views.CropCreateView.as_view(), name='crop_create'),
    path('crops/<int:pk>/edit', views.CropUpdateView.as_view(), name='crop_update'),
    path('crops/<int:pk>/delete/', views.CropDeleteView.as_view(), name='crop_delete'),


    # Field urls
    path('fields/', views.FieldListView.as_view(), name='field_list'),
    path('fields/<int:pk>', views.FieldDetailView.as_view(), name='field_detail'),
    path('fields/add/', views.FieldCreateView.as_view(), name='field_create'),
    path('fields/<int:pk>/edit', views.FieldUpdateView.as_view(), name='field_update'),
    path('fields/<int:pk>/delete/', views.FieldDeleteView.as_view(), name='field_delete'),



    # Planting Calendar urls
    path('activities/', views.ActivityListView.as_view(), name='activity_list'),
    path('activities/<int:pk>', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/add/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('activities/<int:pk>/edit', views.ActivityUpdateView.as_view(), name='activity_update'),
    path('activities/<int:pk>/delete/', views.ActivityDeleteView.as_view(), name='activity_delete'),

    # Weather Record urls
    path('weathers/', views.WeatherRecordListView.as_view(), name='weather_list'),
    path('weathers/<int:pk>', views.WeatherRecordDetailView.as_view(), name='weather_detail'),
    path('weathers/add/', views.WeatherRecordCreateView.as_view(), name='weather_create'),
    path('weathers/<int:pk>/edit', views.WeatherRecordUpdateView.as_view(), name='weather_update'),
    path('weathers/<int:pk>/delete/', views.WeatherRecordDeleteView.as_view(), name='weather_delete'),


    # Route Safety urls
    path('routes/', views.SecureRouteListView.as_view(), name='secure_route_list'),
    path('routes/<int:pk>', views.SecureRouteDetailView.as_view(), name='secure_route_detail'),
    path('routes/add/', views.SecureRouteCreateView.as_view(), name='secure_route_create'),
    path('routes/<int:pk>/edit', views.SecureRouteUpdateView.as_view(), name='secure_route_update'),
    path('routes/<int:pk>/delete/', views.SecureRouteDeleteView.as_view(), name='secure_route_delete'),

    # Registration, Login, Logout Views
    
    path('accounts/profile/',views.ProfileDetail.as_view(template_name='accounts/profile.html'),name='profile'),
    path("registration/", views.SignUpView.as_view(), name='sign_up'),
    # Farmer urls
    path('profiles/', views.FarmerProfileView.as_view(), name='farmer_profile'),
    path('profiles/update/', views.FarmerUpdateView.as_view(), name='farmer_update'),

    #Comment and Post
    path('post/add/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    
    
    # API sections

    path('api/', include(router.urls)),
]

