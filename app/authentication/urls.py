from django.urls import path
from authentication.views import RegisterView,LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView



urlpatterns = [
    path('register/', RegisterView.as_view(),name='register-endpoint'),
    path('logout/', LogoutView.as_view(), name='logout-enpoint'),
    path('login/', TokenObtainPairView.as_view(), name='login-enpoint')

]
