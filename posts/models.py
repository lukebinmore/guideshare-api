from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    def image_dir(self, filename):
        return f"posts/{self.id}/{filename}"

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=50)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    content = models.TextField()
    cover_image = models.ImageField(
        upload_to=image_dir,
        default="/posts/default/placeholder",
    )
    wip = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User, related_name="liked_posts", blank=True
    )
    dislikes = models.ManyToManyField(
        User, related_name="disliked_posts", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def post_likes(self):
        return self.likes.count()

    def post_dislikes(self):
        return self.dislikes.count()


class Category(models.Model):
    title = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title