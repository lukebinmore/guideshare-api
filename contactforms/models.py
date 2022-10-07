from django.db import models
from django.contrib.auth.models import User

REASON_CHOICES = (
    (0, "Support"),
    (1, "Bug Report"),
    (2, "Feedback"),
    (3, "Compliement"),
    (4, "Complaint"),
)

STATUS_CHOICES = (
    (0, "NEW"),
    (1, "OPENED"),
    (2, "IN PROGRESS"),
    (3, "COMPLETE"),
)


class ContactForm(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    email = models.EmailField()
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    reason = models.IntegerField(choices=REASON_CHOICES)
    content = models.TextField(max_length=512)
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.title
