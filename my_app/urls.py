from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path("new-search", views.home, name="home"),
]
