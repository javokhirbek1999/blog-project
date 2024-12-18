from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
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
        # print('Permission are added')


@receiver(post_save, sender=Post)
def make_the_post_link_unique(sender, instance, created, **kwargs):
    if created and Post.objects.filter(slug=instance.slug).count() > 1:
        instance.slug += "-" + str(instance.id)
        instance.save()