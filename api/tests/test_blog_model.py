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

    def test_create_post(self):

        """Test creating a new post instance."""
        
        post = Post.objects.create(**self.post_data)

        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is a test post content.")
        self.assertEqual(post.slug, "test-post")
        self.assertIsNotNone(post.published)

    def test_thumbnail_default(self):

        """Test the default thumbnail is uploaded correctly."""
        
        post = Post.objects.create(**self.post_data)
        self.assertEqual(post.thumbnail.name, "posts/default.jpg")


    def test_post_str_method(self):

        """Test the __str__() method of the Post model."""
        
        post = Post.objects.create(**self.post_data)
        self.assertEqual(str(post), post.title)


    def test_post_permissions(self):

        """Test defined custom permissions in Meta."""
        
        permissions = Post._meta.permissions
        expected_permissions = [
            ('add_own_post', 'Can add own post'),
            ('change_own_post', 'Can change own post'),
            ('delete_own_post', 'Can delete own post'),
        ]
        self.assertEqual(permissions, expected_permissions)
