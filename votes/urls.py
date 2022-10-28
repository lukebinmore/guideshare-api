from django.urls import path
from . import views

# A list of url patterns.
urlpatterns = [
    path("votes/", views.VoteCreate.as_view()),
    path("votes/<int:pk>/", views.VoteDestroy.as_view()),
]
