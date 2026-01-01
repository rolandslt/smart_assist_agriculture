from django.shortcuts import render, redirect
from .models import Farmer, Field, Crop , Activity, WeatherRecord, SecureRoute, Post, Comment, Review
from django.views import generic
from datetime import datetime, timedelta
from .forms import FarmerCreationForm , CommentForm, CropForm, ActivityForm, WeatherRecordForm, SecureRouteForm, FarmerUpdateForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView , ListView , UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth import get_user_model
Farmer = get_user_model() 
# Create your views here.

#----------------
# Home page 
#----------------
def index(request):
    featured_post = Post.objects.first()
    reviews = Review.objects.all().order_by('-created_at')[:5]
   
    can_review = False
    if request.user.is_authenticated:
        one_month_ago = timezone.now() - timedelta(days=30)
        has_recent_review = Review.objects.filter(
            farmer=request.user, 
            created_at__gte=one_month_ago
        ).exists()
        is_old_enough = request.user.date_joined <= one_month_ago
        # If they CAN review, send a message that triggers the popup
        if is_old_enough and not has_recent_review:
            messages.info(request, "show_review_modal")
            can_review = True

    context = {
        'word':'welcome home',
        'reviews': reviews,
        'can_review': can_review,
        'post': featured_post,
        }
    return render(request , 'index.html', context)

#--------------------
# Review 
#--------------------
@login_required
def SubmitReview(request):
    if request.method == 'POST':
        # Safely get the content or an empty string
        content = request.POST.get('content', '').strip()
        
        if content:
            # We use the field name 'farmer' as established earlier
            Review.objects.create(
                farmer=request.user,
                content=content
            )
            return redirect('home')
            
def AllReview(request):
    review_list = Review.objects.all().order_by('-created_at')

    paginator = Paginator(review_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_reviews.html', {'page_obj': page_obj})
#------------------
# Farmer Sin in 
#------------------
class SignUpView(CreateView):
    model= Farmer
    form_class = FarmerCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/sign_up.html'
    

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = Farmer
    template_name = 'accounts/profile.html'
    context_object_name = 'farmer_profile'

    # Override get_object to fetch the currently logged-in user
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['fields'] = Field.objects.filter(farmer=self.request.user)
        return context
    
class FarmerProfileView(LoginRequiredMixin, DetailView):
    model = Farmer
    template_name = 'profiles/farmer_profile.html'
    context_object_name = 'farmer_profile'

    def get_object(self, queryset=None):
        # This tells Django: "Don't look for a PK in the URL, 
        # just use the logged-in user as the data source."
        return self.request.user
    
class FarmerUpdateView(LoginRequiredMixin, UpdateView):
    model = Farmer
    template_name = 'profiles/farmer_form.html'
    form_class = FarmerUpdateForm
    success_url = reverse_lazy('farmer_profile')
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        """Redirects to the profile detail page after a successful update."""
        return reverse_lazy('farmer_profile')


#------------------
# Fields Views
#------------------

class FieldListView(LoginRequiredMixin, ListView):
    """
    Displays a list of all fields belonging to the current logged-in farmer.
    """
    model = Field
    context_object_name = 'fields'
    template_name = 'fields/field_list.html'

    def get_queryset(self):
        """
        Overrides the queryset to filter fields by the currently logged-in user.
        """
        return Field.objects.filter(farmer=self.request.user).annotate(
            crop_count=Count('crops') 
        )

class FieldDetailView(LoginRequiredMixin, DetailView):
    model = Field
    template_name = 'fields/field_detail.html'
    context_object_name = 'field'

    
    
class FieldCreateView(LoginRequiredMixin, CreateView):
    model = Field
    template_name = 'fields/field_form.html'
    fields = ['name','location', 'size_in_hectares', 'soil_type']
    success_url = reverse_lazy('field_list')

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super().form_valid(form)

class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = Field
    template_name ='fields/field_form.html'
    fields = ['name', 'location', 'size_in_hectares', 'soil_type']
    success_url = reverse_lazy('field_list')


    def get_queryset(self):
        return Field.objects.filter(farmer=self.request.user)

class FieldDeleteView(LoginRequiredMixin, DeleteView):
    model = Field
    context_object_name = 'field'
    template_name = 'fields/field_delete_confirm.html'
    success_url = reverse_lazy('field_list')

    def get_queryset(self):
        return Field.objects.filter(farmer=self.request.user)


#------------------
#Crop Views
#------------------

class CropListView(LoginRequiredMixin, ListView):
    model = Crop
    context_object_name = 'crops'
    template_name = 'crops/crop_list.html'

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user).order_by('status', 'expected_harvest')
class CropDetailView(LoginRequiredMixin, DetailView):
    model = Crop 
    context_object_name = 'crop'
    template_name = 'crops/crop_detail.html'

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)

class CropCreateView(LoginRequiredMixin, CreateView):
    model = Crop
    form_class = CropForm 
    template_name = 'crops/crop_form.html'
    success_url = reverse_lazy('crop_list')
    
    # Pass the current farmer to the form for queryset filtering (Step 2)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['farmer'] = self.request.user
        return kwargs

class CropUpdateView(LoginRequiredMixin, UpdateView):
    model = Crop
    template_name = 'crops/crop_form.html'
    form_class = CropForm
    success_url = reverse_lazy('crop_list')
    
    # Pass the current farmer to the form for queryset filtering (Step 2)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['farmer'] = self.request.user
        return kwargs
    
    # Ensure user can only update their own crop
    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)

class CropDeleteView(LoginRequiredMixin, DeleteView):
    model = Crop
    context_object_name = 'crop'
    template_name = 'crops/crop_delete_confirm.html'
    success_url = reverse_lazy('crop_list')

    def get_queryset(self):
        return Crop.objects.filter(fields__farmer=self.request.user)


#------------------
# Planting Calendar Views
#------------------

class ActivityListView(LoginRequiredMixin , ListView):
    model = Activity
    context_object_name = 'activities'
    template_name = 'activities/activity_list.html'

    def get_queryset(self):
        user=self.request.user
        queryset = Activity.objects.filter(farmer=user)
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('scheduled_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the current filter back to the template
        context['current_status'] = self.request.GET.get('status', 'all')
        context['status_choices'] = Activity.STATUS_CHOICES 
        return context
    
class ActivityDetailView(generic.DetailView):
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/activity_detail.html'

    def get_queryset(self):
        return Activity.objects.filter(farmer=self.request.user)
    
class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = Activity
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activity_list')
    form_class = ActivityForm

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filter the Field queryset to only include fields belonging to the current farmer
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        form.fields['crop'].queryset = Crop.objects.filter(fields__farmer=self.request.user).distinct()
        return form


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/activity_form.html'
    success_url = reverse_lazy('activity_list')

    def get_queryset(self):
        return Activity.objects.filter(farmer=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        form.fields['crop'].queryset = Crop.objects.filter(fields__farmer=self.request.user).distinct()
        return form
    

class ActivityDeleteView(LoginRequiredMixin, DeleteView):
    model = Activity
    context_object_name = 'activity'
    template_name = 'activities/activity_delete_confirm.html'
    success_url = reverse_lazy('activity_list')

    def get_queryset(self):
        return Activity.objects.filter(farmer=self.request.user)   


#-----------------------------
# wWeather view Record
#------------------------------
class WeatherRecordListView(LoginRequiredMixin, ListView):
    model = WeatherRecord
    context_object_name = 'weather_records'
    template_name = 'weather/weather_list.html'
    paginate_by = 25
    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)

class WeatherRecordDetailView(LoginRequiredMixin, DetailView):
    model = WeatherRecord
    context_object_name = 'weather_record'
    template_name = 'weather/weather_detail.html'

    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)
    
class WeatherRecordCreateView(LoginRequiredMixin, CreateView):
    model = WeatherRecord
    template_name = 'weather/weather_form.html'
    form_class = WeatherRecordForm
    success_url = reverse_lazy('weather_list')

    def form_valid(self, form):
        form.instance.farmer = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        return form
    
class WeatherRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = WeatherRecord
    template_name = 'weather/weather_form.html'
    form_class = WeatherRecordForm
    success_url = reverse_lazy('weather_list')
    context_object_name = 'weather_record'

    def form_valid(self, form):
        form.instance.farmer = self.request.User
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['field'].queryset = Field.objects.filter(farmer=self.request.user)
        return form
    
    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)
    

class WeatherRecordDeleteView(LoginRequiredMixin, DeleteView):
    model = WeatherRecord
    context_object_name = 'weather_record'
    template_name = 'weather/weather_delete_confirm.html'
    success_url = reverse_lazy('weather_list')
    
    def get_queryset(self):
        return WeatherRecord.objects.filter(farmer=self.request.user)
    
#------------------
# Route Safety Record Views
#------------------

class SecureRouteListView(LoginRequiredMixin, ListView):
    model = SecureRoute
    context_object_name='secure_route_list'
    template_name = 'routes/secure_route_list.html'

    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)
class SecureRouteDetailView(LoginRequiredMixin, DetailView):
    model = SecureRoute
    context_object_name='secure_route_detail'
    template_name = 'routes/secure_route_detail.html'


    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)
    
class SecureRouteCreateView(LoginRequiredMixin, CreateView):
    model = SecureRoute
    template_name = 'routes/secure_route_form.html'
    success_url = reverse_lazy('secure_route_list')
    form_class = SecureRouteForm

    def form_valid(self, form):
        form.instance.farmer = self.request.user 
        return super().form_valid(form)
        
class SecureRouteUpdateView(LoginRequiredMixin, UpdateView):
    model = SecureRoute
    name='secure_route_update'
    template_name = 'routes/secure_route_form.html'
    success_url = reverse_lazy('secure_route_list')
    fields = ['route_name', 'route_path_geojson', 'security_status', 'risk_notes']

    def form_valid(self, form):
        form.instance.farmer = self.request.user 
        return super().form_valid(form)
    
    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user)

class SecureRouteDeleteView(LoginRequiredMixin, DeleteView):
    model = SecureRoute
    context_object_name = 'secure_route_delete'
    template_name = 'routes/secure_route_delete_confirm.html'
    success_url = reverse_lazy('secure_route_list')

    def get_queryset(self):
        return SecureRoute.objects.filter(farmer=self.request.user) 


#------------------------------------
# Post ,Comments and Review Views
#------------------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model= Post
    template_name = 'blog/post_form.html'
    context_object_name = 'post'
    fields = ['title', 'content']
    
    
    def form_valid(self, form):
        form.instance.author = self.request.User
    
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        return context

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model:Post
    context_object_name = 'post_delete'
    template_name = 'blog/post_delete_confirm.html'
    success_url = reverse_lazy('home') 


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id =self.kwargs['post_id']
        
        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            form.instance.parent_id = parent_id
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['post_id']})
    
