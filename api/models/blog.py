from django.db import models
from django.contrib.auth import get_user_model



def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)



class Post(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to=upload_to, default='posts/default.jpg')
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique_for_date='published')
    published = models.DateTimeField(auto_now_add=True)


    objects = models.Manager()

    class Meta:
        ordering = ('-published',)
        permissions = [
            ('add_own_post', 'Can add own post'),
            ('change_own_post', 'Can change own post'),
            ('delete_own_post', 'Can delete own post'),
        ]
    

    def __str__(self):
        return self.title
