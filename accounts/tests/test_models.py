from django.test import TestCase
from accounts.models import CustomUser


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        email = "test@example.com"
        first_name = "John"
        last_name = "Doe"
        user = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name)

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        email = "admin@example.com"
        first_name = "Admin"
        last_name = "User"
        user = CustomUser.objects.create_superuser(email=email, first_name=first_name, last_name=last_name)

        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_str_representation(self):
        email = "test@example.com"
        user = CustomUser.objects.create_user(email=email)

        self.assertEqual(str(user), email)
