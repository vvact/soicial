from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthenticationTests(APITestCase):
    
    def setUp(self):
        """Create a test user before each test"""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword123"
        )
        self.login_url = "/api/auth/login/"
        self.register_url = "/api/auth/register/"
        self.logout_url = "/api/auth/logout/"
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        """Test user login"""
        data = {
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
    
    # def test_token_refresh(self):
    #     """Test JWT token refresh"""
    #     refresh = RefreshToken.for_user(self.user)
    #     response = self.client.post(self.token_refresh_url, {"refresh": str(refresh)})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("access", response.data)

    def test_user_logout(self):
        """Test user logout"""
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.post(self.logout_url, {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

