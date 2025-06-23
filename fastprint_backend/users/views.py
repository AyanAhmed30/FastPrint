import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import *
from .tokens import email_verification_token
from .utils import send_verification_email, send_password_reset_email


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())
            token = email_verification_token.make_token(user)
            send_verification_email(user, uidb64, token)
            return Response({"message": "Registered successfully. Please check your email to verify your account."}, status=201)
        return Response(serializer.errors, status=400)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and email_verification_token.check_token(user, token):
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if not user.is_verified:
                return Response({'error': 'Email not verified.'}, status=status.HTTP_401_UNAUTHORIZED)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'is_admin': user.is_admin,
                }
            })
        return Response(serializer.errors, status=400)


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(User, email=serializer.validated_data['email'])
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())
            token = PasswordResetTokenGenerator().make_token(user)
            send_password_reset_email(user, uidb64, token)
            return Response({'message': 'Reset link sent to your email'})
        return Response(serializer.errors, status=400)


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid link'}, status=400)

        if PasswordResetTokenGenerator().check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({'message': 'Password reset successful'})
            return Response(serializer.errors, status=400)
        return Response({'error': 'Invalid or expired token'}, status=400)
