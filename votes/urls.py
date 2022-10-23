from django.urls import path
from . import views

urlpatterns = [
    path("votes/", views.VoteCreate.as_view()),
    path("votes/<int:pk>/", views.VoteDestroy.as_view()),
]
