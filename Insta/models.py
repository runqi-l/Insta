from django.db import models
from imagekit.models import ProcessedImageField
# Create your models here.

class Post(models.Model):
    title = models.TextField(blank=True, null=True) #no title or blank is fine
    image = ProcessedImageField(
        upload_to='static/image/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
    )

class PostTwo(models.Model):
    title = models.TextField(blank=True, null=True) #no title or blank is fine
    image = ProcessedImageField(
        upload_to='static/image/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
    )
