from .models import Quiz, Choice
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.http import HttpResponse


# @csrf_exempt
# def index(request):
#     quiz = Quiz.objects.all()
#     data = [i.user for i in quiz]

#     return HttpResponse(quiz[0].user.username)


class QuizListView(ListView):

    model = Quiz
    pagenate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
