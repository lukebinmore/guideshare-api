from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment

CHOICES = ((0, "like"), (1, "dislike"))


class Vote(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_votes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="post_votes",
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="comment_votes",
    )
    vote = models.IntegerField(choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = [
            ["owner", "post", "vote"],
            ["owner", "comment", "vote"],
        ]

    def __str__(self):
        vote = "like" if self.vote == "like" else "dislike"
        item = self.post.id if self.post else self.comment.id
        return f"{self.owner} {vote}'d {item}"
