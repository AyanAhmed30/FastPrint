from django.urls import path
from .views import (
    RegisterView, LoginView, VerifyEmailView,
    PasswordResetRequestView, PasswordResetView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # ✅ FIXED: Include uidb64 and token in the verify link
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    
    path('request-reset-password/', PasswordResetRequestView.as_view(), name='request-reset-password'),
    
    # ✅ FIXED: uidb64 instead of uid
    path('reset-password/<uidb64>/<token>/', PasswordResetView.as_view(), name='reset-password'),
]
