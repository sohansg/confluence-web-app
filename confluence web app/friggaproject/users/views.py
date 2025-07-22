from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.generics import ListAPIView
from users.models import User
from users.serializers import UserSerializer
from .utils import generate_reset_token, verify_reset_token
from django.core.mail import send_mail
from django.conf import settings

# ✅ User Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ User List View (for listing all users)
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# ✅ Forgot Password API – Sends reset link to email
class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            uid, token = generate_reset_token(user)
            reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"  # Change for production
            send_mail(
                subject="Reset Your Password",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
        return Response({"message": "If user exists, password reset link has been sent."}, status=status.HTTP_200_OK)


# ✅ Reset Password API – Accepts new password via token link
class ResetPasswordAPIView(APIView):
    def post(self, request, uidb64, token):
        new_password = request.data.get("password")
        user = verify_reset_token(uidb64, token)
        if not user:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
