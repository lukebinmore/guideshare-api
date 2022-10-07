from django.urls import path
from . import views

urlpatterns = [
    path("contact-form/", views.ContactForm.as_view()),
]
