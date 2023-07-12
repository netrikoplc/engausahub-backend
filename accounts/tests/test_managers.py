from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserManagerTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        manager = User.objects
        email = "test@example.com"
        password = "testpassword"
        user = manager.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        manager = User.objects
        email = "admin@example.com"
        password = "adminpassword"
        user = manager.create_superuser(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

        with self.assertRaises(ValueError):
            manager.create_superuser(email=email, password=password, is_staff=False)

        with self.assertRaises(ValueError):
            manager.create_superuser(email=email, password=password, is_superuser=False)
