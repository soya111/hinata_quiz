from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Quiz(models.Model):
    title = models.TextField(max_length=50, verbose_name="クイズタイトル")
    statement = models.TextField(max_length=200, verbose_name="問題文")
    thumbnail_image_url = models.URLField(
        max_length=1000, verbose_name="画像URL")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False, verbose_name='認証ステータス')
    is_public = models.BooleanField(default=False, verbose_name='公開ステータス')

    def __str__(self):
        return self.statement + ' '.join([i.text for i in self.get_choices()])

    def choices_str(self):
        return ' '.join([i.text for i in self.get_choices()])

    def get_choices(self):
        return Choice.objects.filter(quiz_id=self.id).all().order_by('?')


class Choice(models.Model):
    quiz = models.ForeignKey(
        Quiz, related_name='choices', on_delete=models.CASCADE)
    text = models.TextField(max_length=50)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Nonce(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    nonce = models.CharField(max_length=200)

    def __str__(self):
        return self.nonce


class UserInfo(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    line_id = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
