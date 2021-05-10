from django.urls import path
from . import views

app_name = 'kittywallet'
urlpatterns = [
    path('', views.MainView.as_view(), name='main')
]