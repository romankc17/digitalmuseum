from django.urls import path

from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOTP.as_view(), name='verify-otp'),
    path('send-verification-otp/', views.SendVerificationOTP.as_view(), name='send-verification-otp'),
    
    path('login/', 
         views.CustomTokenObtainPairView.as_view(), 
         name='token_create'),  # override sjwt stock token
    path('token/refresh/', 
         jwt_views.TokenRefreshView.as_view(), 
         name='token_refresh'),
]