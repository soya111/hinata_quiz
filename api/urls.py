from django.urls import path

from . import views, main, web
from .web import QuizListView

urlpatterns = [
    # path('', views.index, name='callback'),
    path('api/', main.index, name='main_index'),
    path('quiz/', QuizListView.as_view(), name='quiz-list'),
    # path('web/', web.index, name='quiz-list'),
    path('show_linebot_log/', views.show_linebot_log, name='show_linebot_log'),
    path('show_debug_log/', views.show_debug_log, name='show_debug_log'),
]
