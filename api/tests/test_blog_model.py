from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from api.models.blog import Post  


class PostModelTest(TestCase):

    def setUp(self):

        """Set up the dumy test data."""
        
        self.user = get_user_model().objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            password="password123"
        )

        self.post_data = {
            "author": self.user,
            "title": "Test Post",
            "content": "This is a test post content.",
            "slug": "test-post",
        }
