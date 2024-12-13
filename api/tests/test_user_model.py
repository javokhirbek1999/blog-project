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

    