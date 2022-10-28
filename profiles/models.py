from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from django.db.models.signals import post_save, pre_delete


# It creates a model for Profiles
class Profile(models.Model):
    def image_dir(self, filename):
        return f"profiles/{self.owner.id}/{filename}"

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=25, blank=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    picture = models.ImageField(
        upload_to=image_dir,
        default="/profiles/default/placeholder",
    )
    following = models.ManyToManyField(
        "self", related_name="followers", blank=True, symmetrical=False
    )
    saved_posts = models.ManyToManyField(
        Post, related_name="post_saves", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        """
        The __str__ method should return a string representation of the object
        :return: The owner's name and the comment's id.
        """
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    If a user is created, create a profile for that user

    :param sender: The model class
    :param instance: The instance of the model that was just created
    :param created: A boolean; True if a new record was created
    """
    if created:
        Profile.objects.create(
            owner=instance,
        )


def disable_account(sender, instance, **kwargs):
    """
    If the user's account is disabled, then disable the user's account

    :param sender: The model class
    :param instance: The instance being saved
    """
    user = User.objects.filter(id=instance.owner.id).first()
    user.is_active = False
    user.save()


# Connecting the signals to the functions.
post_save.connect(create_profile, sender=User)
pre_delete.connect(disable_account, sender=Profile)
