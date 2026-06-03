from django.urls import path
from authentication.views import RegisterView, ProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView



urlpatterns = [
    path('register/', RegisterView.as_view(),name='register-endpoint'),
    path('login/', TokenObtainPairView.as_view(), name='login-enpoint'),    
    path('logout/',TokenBlacklistView.as_view(),name='logout-endpoint'),
    path('profile/', ProfileView.as_view(), name='profile-endpoint'),
]
