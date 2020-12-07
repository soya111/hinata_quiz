from django.db import models

# Create your models here.


class Quiz(models.Model):
    title = models.TextField(max_length=50)
    statement = models.TextField(max_length=200)
    thumbnail_image_url = models.URLField(max_length=1000)


class Choice(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='choices', on_delete=models.CASCADE)
    text = models.TextField(max_length=50)
    is_correct = models.BooleanField(default=False)
