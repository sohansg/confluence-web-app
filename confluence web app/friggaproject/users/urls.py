from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    UserListView,
    ForgotPasswordAPIView,
    ResetPasswordAPIView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),

    # ✅ New forgot & reset password routes
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/<str:uidb64>/<str:token>/', ResetPasswordAPIView.as_view(), name='reset-password'),
]
