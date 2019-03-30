from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question-input', views.question_input, name='question-input')
]
