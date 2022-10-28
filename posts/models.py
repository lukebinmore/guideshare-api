from django.db import models
from django.contrib.auth.models import User


# It creates a model for Posts
class Post(models.Model):
    def image_dir(self, filename):
        """
        It returns a string that is the path to the image file

        :param filename: The name of the file that was uploaded
        :return: The path to the image file.
        """
        return f"posts/{self.owner.id}/{filename}"

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        """
        The __str__ method should return a string representation of the object
        :return: The owner's name and the comment's id.
        """
        return self.title

    def post_likes(self):
        """
        It returns the number of votes with a value of 0 for the post
        :return: The number of votes for a post that are equal to 0.
        """
        return self.post_votes.filter(vote=0).count()

    def post_dislikes(self):
        """
        It returns the number of votes with a value of 1 for the post
        :return: The number of votes that are equal to 1.
        """
        return self.post_votes.filter(vote=1).count()


# It creates a model for the database.
class Category(models.Model):
    title = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        The __str__ method should return a string representation of the object
        :return: The owner's name and the comment's id.
        """
        return self.title
