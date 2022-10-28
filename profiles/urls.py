from django.urls import path
from . import views

# A list of url patterns.
urlpatterns = [
    path("profiles/<int:pk>/", views.ProfileDetail.as_view()),
    path("profiles/", views.ProfileList.as_view()),
    path("saved-following/<int:pk>/", views.SavedFollowing.as_view()),
]
