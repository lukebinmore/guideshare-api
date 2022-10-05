from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete


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
        User, related_name="followers", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            owner=instance,
        )


def disable_account(sender, instance, **kwargs):
    user = User.objects.filter(id=instance.owner.id).first()
    user.is_active = False
    user.save()


post_save.connect(create_profile, sender=User)
pre_delete.connect(disable_account, sender=Profile)
