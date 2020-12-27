from django.urls import path

from . import views, main, web
from .web import QuizListView, QuizDetailView, SignUpView, QuizCreateView, UserQuizListView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('api/', main.index, name='main_index'),
    path('', QuizListView.as_view(), name='quiz-list'),
    path('quiz/', QuizListView.as_view(), name='quiz-list'),
    path('quiz/add/', QuizCreateView.as_view(), name='quiz-add'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz/<int:id>/edit/', web.edit, name='quiz-edit'),
    path('account/', UserQuizListView.as_view(), name='account'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('show_linebot_log/', views.show_linebot_log, name='show_linebot_log'),
    path('show_debug_log/', views.show_debug_log, name='show_debug_log'),
]
