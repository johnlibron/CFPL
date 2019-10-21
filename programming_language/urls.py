from django.urls import path
from programming_language import views

urlpatterns = [
    path('', views.index, name="index"),
]