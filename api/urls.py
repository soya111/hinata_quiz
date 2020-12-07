from django.urls import path

from . import views, main, web

urlpatterns = [
    # path('', views.index, name='callback'),
    path('', main.index, name='main_index'),
    path('web/', web.index, name='web_index'),
    path('show_linebot_log/', views.show_linebot_log, name='show_linebot_log'),
    path('show_debug_log/', views.show_debug_log, name='show_debug_log'),
]
