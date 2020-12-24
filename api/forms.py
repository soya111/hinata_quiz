from django.forms import ModelForm
from .models import Quiz, Choice


class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'statement', 'thumbnail_image_url']


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']
