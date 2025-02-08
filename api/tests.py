from datetime import timedelta
from time import sleep

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserAPITest(APITestCase):

    def setUp(self):
        self.register_url = "/api/register/"
        self.login_url = "/api/login/"
        self.refresh_url = "/api/refresh/"
        self.logout_url = "/api/logout/"
        self.me_url = "/api/me/"
        self.user_data = {
            "email": "test1@example.com",
            "password": "password123",
            "username": "testuser",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        response = self.client.post(
            self.register_url,
            {
                "email": "test2@example.com",
                "password": "password",
                "username": "",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        response = self.client.post(
            self.login_url,
            {
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.data)

    def test_access_token_refresh(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            self.refresh_url, {"refresh_token": str(refresh)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_user_logout(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(
            self.logout_url, {"refresh_token": str(refresh)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], "User logged out.")

    def test_retrieve_personal_information(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_update_personal_information(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(self.me_url, {"username": "UpdatedUser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "UpdatedUser")

    def test_user_registration_invalid_data(self):
        response = self.client.post(
            self.register_url,
            {
                "email": "test3@example.com",
                "username": "testuser",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_missing_email(self):
        response = self.client.post(
            self.register_url,
            {
                "password": "password123",
                "username": "testuser_without_email",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_user_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_token_refresh_invalid_token(self):
        invalid_token = "invalid.token.value"
        response = self.client.post(
            self.refresh_url, {"refresh_token": invalid_token}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
        self.assertEqual(
            response.data["error"], "Invalid token or expired refresh token"
        )

    def test_user_logout_invalid_token(self):
        response = self.client.post(
            self.logout_url, {"refresh_token": "invalid_token"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Token is invalid or expired")

    def test_retrieve_personal_information_without_authentication(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_personal_information_without_authentication(self):
        response = self.client.put(self.me_url, {"username": "NewName"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_token_expiry(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(seconds=1))
        sleep(2)
        response = self.client.get(
            self.me_url, HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
