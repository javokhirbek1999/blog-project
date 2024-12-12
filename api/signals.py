from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from api.models import User, Post


@receiver(post_save, sender=User)
def assign_custom_permissions(sender, instance, created, **kwargs):
    """
    Assign custom permissions to a user after they are created.
    """
    if created:  # Only assign permissions to newly created users
        content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(content_type=content_type, codename__in=[
            'add_own_post', 'change_own_post', 'delete_own_post'
        ])
        instance.user_permissions.add(*permissions)
        instance.save()
        print('Permission are added')
