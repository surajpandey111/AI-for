from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot_view'),
    path('chatbot/', views.chatbot_response, name='chatbot_response'),
]