from django.urls import path
from . import views

# A list of url patterns.
urlpatterns = [
    path("contact-form/", views.ContactForm.as_view()),
]
