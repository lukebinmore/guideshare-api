from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


# It creates a model for Comments
class Comment(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        """
        The __str__ method should return a string representation of the object
        :return: The owner's name and the comment's id.
        """
        return f"{self.owner}'s Comment #{self.id}"

    def comment_likes(self):
        """
        It returns the number of comment votes that are "like" for a given
        comment
        :return: The number of votes that are "like"
        """
        return self.comment_votes.filter(vote="like").count()

    def comment_dislikes(self):
        """
        It returns the number of comment votes that are "dislike" for a given
        comment
        :return: The number of votes that are "dislike"
        """
        return self.comment_votes.filter(vote="dislike").count()
