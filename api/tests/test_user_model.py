from django.test import TestCase
from django.core.exceptions import ValidationError
from api.models.user import User


class UserModelTest(TestCase):
    def setUp(self):
        
        """Set up the dumy data for test."""
        
        self.first_name = "John"
        self.last_name = "Doe"
        self.email = "john.doe@example.com"
        self.password = "securepassword123"

    def test_create_user(self):

        """Test creating a regular user."""
        
        user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)
        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):

        """Test creating a superuser(admin user)."""
        
        superuser = User.objects.create_superuser(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password
        )

        self.assertEqual(superuser.first_name, self.first_name)
        self.assertEqual(superuser.last_name, self.last_name)
        self.assertEqual(superuser.email, self.email)
        self.assertTrue(superuser.check_password(self.password))
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_without_email(self):

        """Test creating a user without an email raises a ValueError."""
        
        with self.assertRaisesMessage(ValueError, "Email is required, please enter your email"):
            User.objects.create_user(
                first_name=self.first_name,
                last_name=self.last_name,
                email=None,
                password=self.password
            )

    def test_email_normalization(self):

        """Test the email for a new user is normalized."""
        
        email = "Test.Email@Example.Com"
        user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email=email,
            password=self.password
        )
        self.assertEqual(user.email, email.lower())

    def test_required_fields(self):

        """Test the required fields are enforced."""
        
        with self.assertRaises(ValidationError):
            user = User(first_name=self.first_name, last_name=self.last_name)
            user.full_clean()  # Validate the model instance without saving the instance
