from django.urls import path
from . import views

# A list of url patterns.
urlpatterns = [
    path("comments/", views.CommentList.as_view()),
    path("comments/<int:pk>/", views.CommentDetail.as_view()),
]
