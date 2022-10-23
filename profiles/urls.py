from django.urls import path
from . import views

urlpatterns = [
    path("profiles/<int:pk>/", views.ProfileDetail.as_view()),
    path("profiles/", views.ProfileList.as_view()),
    path("saved-posts/<int:pk>/", views.SavedPostsList.as_view()),
]
