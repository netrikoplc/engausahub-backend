from django.test import TestCase
from rest_framework.exceptions import ValidationError
from accounts.serializers import CustomLoginSerializer, CustomRegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory
from django.test.client import RequestFactory
from allauth.account.models import EmailAddress


class CustomLoginSerializerTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.email_address = EmailAddress.objects.create(
            email=self.user.email, user=self.user, verified=True, primary=True
        )

    def test_valid_data(self):
        request = self.factory.post("/accounts/login/", data={"email": "test@example.com", "password": "testpassword"})
        serializer = CustomLoginSerializer(data=request.POST, context={"request": request})
        self.assertTrue(serializer.is_valid())
        self.assertIn("email", serializer.validated_data)
        self.assertEqual(serializer.validated_data["email"], "test@example.com")


class CustomRegisterSerializerTest(TestCase):
    def test_cleaned_data(self):
        serializer = CustomRegisterSerializer(
            data={
                "email": "test1@example.com",
                "password1": "testpassword",
                "password2": "testpassword",
                "first_name": "John",
                "last_name": "Doe",
            }
        )
        self.assertTrue(serializer.is_valid())
        cleaned_data = serializer.get_cleaned_data()
        self.assertIn("first_name", cleaned_data)
        self.assertIn("last_name", cleaned_data)
        self.assertEqual(cleaned_data["first_name"], "John")
        self.assertEqual(cleaned_data["last_name"], "Doe")

    def test_missing_required_fields(self):
        serializer = CustomRegisterSerializer(
            data={"email": "test@example.com", "password1": "testpassword", "password2": "testpassword"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)
