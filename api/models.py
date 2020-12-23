from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.TextField(max_length=50)
    statement = models.TextField(max_length=200)
    thumbnail_image_url = models.URLField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.statement

    def get_choices(self):
        return Choice.objects.filter(quiz_id=self.id).all().order_by('?')


class Choice(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='choices', on_delete=models.CASCADE)
    text = models.TextField(max_length=50)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
