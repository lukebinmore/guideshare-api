from rest_framework.test import APITestCase
from rest_framework import status
from .models import Vote
from posts.models import Post, Category
from comments.models import Comment
from django.contrib.auth.models import User


# Tests for the vote create view
class VoteCreateViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="peter", password="pass")
        peter = User.objects.get(username="peter")
        Category.objects.create(title="Category Title")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=1, owner=peter, category=category, content="Post Content"
        )
        Post.objects.create(
            id=2, owner=peter, category=category, content="Second Post Content"
        )
        post = Post.objects.get(id=1)
        Comment.objects.create(
            id=1, owner=peter, post=post, content="Comment Content"
        )
        Vote.objects.create(id=1, owner=peter, post=post, vote=0)

    def test_users_can_create_post_votes(self):
        self.client.login(username="peter", password="pass")
        response = self.client.post(
            "/votes/", {"post": 2, "comment": "", "vote": 0}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_users_cant_create_diplicate_votes(self):
        self.client.login(username="peter", password="pass")
        response = self.client.post(
            "/votes/", {"post": 1, "comment": "", "vote": 0}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_users_can_create_comment_votes(self):
        self.client.login(username="peter", password="pass")
        response = self.client.post(
            "/votes/", {"post": "", "comment": 1, "vote": 0}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# Tests for the vote delete view
class VoteDestroyViewTests(APITestCase):
    def setUp(self):
        """
        Setup for following view tests
        """
        User.objects.create_user(username="peter", password="pass")
        peter = User.objects.get(username="peter")
        Category.objects.create(title="Category Title")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=1, owner=peter, category=category, content="Post Content"
        )
        post = Post.objects.get(id=1)
        Comment.objects.create(
            id=1, owner=peter, post=post, content="Comment Content"
        )
        Vote.objects.create(id=1, owner=peter, post=post, vote=0)

    def test_users_can_delete_own_votes(self):
        self.client.login(username="peter", password="pass")
        response = self.client.delete("/votes/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_cant_delete_others_votes(self):
        self.client.login(username="steve", password="pass")
        response = self.client.delete("/votes/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
