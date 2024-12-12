from django.db import models
from django.contrib.auth import get_user_model



def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)



class Post(models.Model):

    title = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to=upload_to, default='posts/default.jpg')
    content = models.TextField()
    slug = models.SlugField(max_length=200, unique_for_date='published')
    published = models.DateTimeField(auto_now_add=True)


    objects = models.Manager()

    class Meta:
        ordering = ('-published',)
    

    def __str__(self):
        return self.title
