from .models import Quiz, Choice
from .forms import QuizForm, ChoiceForm
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
import json


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
    template_name = 'api/quiz_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)

        if quiz.is_approved == False and quiz.user != request.user:
            return HttpResponse("権限がありません。ログインしてください。", status=403)

        context = {
            'object': quiz
        }
        return render(request, self.template_name, context)


class QuizCreateView(CreateView, LoginRequiredMixin):
    template_name = 'api/quiz_add.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('quiz-add'))
        context = {
            'quiz_form': QuizForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login') + '?next=' + reverse('quiz-add'))

        choices = [
            request.POST['incorrect_choice-{}'.format(i)] for i in range(1, 4)]

        # choiceのバリデーション
        if request.POST['correct_choice'] == '' or not any(choices):
            return HttpResponse("400", status="400")

        quiz = Quiz(title=request.POST['title'],
                    statement=request.POST['statement'], thumbnail_image_url=request.POST['thumbnail_image_url'], user=request.user)
        quiz.save()

        choice = Choice(
            quiz=quiz, text=request.POST['correct_choice'], is_correct=True)
        choice.save()

        for i in choices:
            if not i:
                break
            choice = Choice(quiz=quiz, text=i, is_correct=False)
            choice.save()

        return HttpResponseRedirect(reverse('quiz-detail', args=[quiz.id]))


@login_required()
def edit(request, id):
    quiz = Quiz.objects.get(id=id)
    if quiz.user != request.user:
        return HttpResponse("権限がありません。ログインしてください。", status=403)

    if request.method == "GET":
        template_name = 'api/quiz_edit.html'

        choices = quiz.get_choices()
        correct_choice = list(filter(lambda x: x.is_correct == True, choices))
        incorrect_choices = list(
            filter(lambda x: x.is_correct == False, choices))
        context = {
            'quiz': quiz,
            'form': QuizForm(instance=quiz),
            'correct_choice': correct_choice[0],
            'incorrect_choices': incorrect_choices
        }
        return render(request, template_name, context)

    elif request.method == "POST":
        quiz.title = request.POST['title']
        quiz.statement = request.POST['statement']
        quiz.thumbnail_image_url = request.POST['thumbnail_image_url']
        quiz.is_approved = False
        quiz.save()

        dict_post = dict(request.POST)

        correct_choice = Choice.objects.get(id=int(dict_post['ccid'][0]))
        correct_choice.text = dict_post['cc'][0]
        correct_choice.save()

        for i, value in enumerate(dict_post['icid']):
            incorrect_choice = Choice.objects.get(id=int(value))
            incorrect_choice.text = dict_post['ic'][i]
            incorrect_choice.save()

        return HttpResponseRedirect(reverse('quiz-detail', args=[id]))

        # class QuizUpdateView(UpdateView):

        #     model = Quiz

        #     fields = ['title', 'statement', 'thumbnail_image_url']
        #     template_name = 'api/quiz_edit.html'


class UserQuizListView(ListView, LoginRequiredMixin):
    model = Quiz
    template_name = 'api/account.html'

    def get(self, request):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        quiz_list = Quiz.objects.filter(user=request.user)
        context = {
            'object_list': quiz_list
        }
        return render(request, self.template_name, context)
