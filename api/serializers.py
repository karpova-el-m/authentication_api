from django.contrib.auth import get_user_model
from rest_framework import serializers, status
from rest_framework.response import Response

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "username"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"required": False},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            username=(
                validated_data.get("username")
                if validated_data.get("username")
                else validated_data["email"]
            ),
        )

    def validate_username(self, value):
        if not value:
            return self.initial_data.get("email")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(
                {"email": "This field is required."}
            )
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("username", None)
        return representation


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):

    def get(self, request):
        try:
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    class Meta:
        model = User
        fields = ["id", "email", "username"]
