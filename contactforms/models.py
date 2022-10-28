from django.db import models

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


# It creates a model for Contact Forms
class ContactForm(models.Model):
    title = models.CharField(max_length=50)
    username = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    reason = models.IntegerField(choices=REASON_CHOICES)
    content = models.TextField(max_length=512)
    status = models.IntegerField(choices=STATUS_CHOICES, default="0")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        """
        The __str__ method should return a string representation of the object
        :return: The owner's name and the comment's id.
        """
        return self.title
