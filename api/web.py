from .models import Quiz, Choice
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def index(request):
    quiz = Quiz.objects.all()
    data = [i.statement for i in quiz]

    return HttpResponse(data)
