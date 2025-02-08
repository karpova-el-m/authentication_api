from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (LoginSerializer, LogoutSerializer,
                          RegisterSerializer, TokenRefreshSerializer,
                          UserDetailSerializer)

User = get_user_model()


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError:
            raise


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(
                email=serializer.validated_data["email"]
            ).first()
            if user and user.check_password(
                serializer.validated_data["password"]
            ):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh),
                    }
                )
        return Response(
            {"error": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh_token = serializer.validated_data["refresh_token"]
                token = RefreshToken(refresh_token)
                return Response(
                    {
                        "access_token": str(token.access_token),
                        "refresh_token": str(token),
                    }
                )
            except TokenError:
                return Response(
                    {"error": "Invalid token or expired refresh token"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh_token"]
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {"success": "User logged out."}, status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserDetailSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
