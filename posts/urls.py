from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostList.as_view()),
    path("posts/<int:pk>/", views.PostDetail.as_view()),
    path("posts/create/", views.PostCreate.as_view()),
    path("posts/categories/", views.CategoryList.as_view()),
]
