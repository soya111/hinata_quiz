from .models import Quiz, Choice
from .forms import QuizForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse


# @csrf_exempt
# def index(request):
#     quiz = Quiz.objects.all()
#     data = [i.user for i in quiz]

#     return HttpResponse(quiz[0].user.username)

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'api/signup.html'


class QuizListView(ListView):

    model = Quiz
    pagenate_by = 10

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(is_approved=True)


class QuizDetailView(DetailView):

    model = Quiz

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def edit(request, id):
    quiz = Quiz.objects.get(id=id)
    if quiz.user != request.user:
        return HttpResponse("権限がありません", status=403)

    if request.method == "GET":
        template_name = 'api/quiz_edit.html'
        context = {
            'quiz': quiz,
            'form': QuizForm(instance=quiz)
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        quiz.title = request.POST['title']
        quiz.statement = request.POST['statement']
        quiz.thumbnail_image_url = request.POST['thumbnail_image_url']
        quiz.save()
        # if form.is_valid():
        #     form.save()
        return HttpResponseRedirect(reverse('quiz-detail', args=[id]))

        # class QuizUpdateView(UpdateView):

        #     model = Quiz

        #     fields = ['title', 'statement', 'thumbnail_image_url']
        #     template_name = 'api/quiz_edit.html'
