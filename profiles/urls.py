from django.urls import path
from . import views

urlpatterns = [
    path("profile/<int:pk>/", views.ProfileDetail.as_view()),
]
