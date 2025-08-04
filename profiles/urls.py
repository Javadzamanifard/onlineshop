from django.urls import path
from .views import ProfileDetailView, profile_update_view

app_name = 'profiles'

urlpatterns = [
    path('edit/', profile_update_view, name='update'),
    path('<slug:slug>/', ProfileDetailView.as_view(), name='detail'),
]