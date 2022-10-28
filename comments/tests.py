from rest_framework.test import APITestCase
from rest_framework import status
from .models import Comment
from posts.models import Post, Category
from django.contrib.auth.models import User


class CommentListViewTests(APITestCase):
    def setUp(self):
        peter = User.objects.create_user(username="peter", password="pass")
        Category.objects.create(id=1, title="Category Title")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=1,
            owner=peter,
            title="Post Title",
            category=category,
            content="",
        )
        post = Post.objects.get(id=1)
        Comment.objects.create(owner=peter, post=post, content="First Content")
        Comment.objects.create(
            owner=peter, post=post, content="Second Content"
        )

    def test_can_list_comments(self):
        peter = User.objects.get(username="peter")
        post = Post.objects.get(id=1)
        Comment.objects.create(owner=peter, post=post, content="Third Comment")
        response = self.client.get("/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_list_filtered_comments(self):
        peter = User.objects.get(username="peter")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=2,
            owner=peter,
            title="Second Post Title",
            category=category,
            content="",
        )
        post = Post.objects.get(id=2)
        Comment.objects.create(
            owner=peter, post=post, content="Fourth Content"
        )
        response = self.client.get("/comments/?post=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username="peter", password="pass")
        response = self.client.post(
            "/comments/", {"post": 1, "content": "Fifth Comment"}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_comments(self):
        response = self.client.post(
            "/comments/", {"post": 1, "content": "Third Comment Test"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        peter = User.objects.create_user(username="peter", password="pass")
        steve = User.objects.create_user(username="steve", password="pass")
        Category.objects.create(id=1, title="Category Title")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=1,
            owner=peter,
            title="Post Title",
            category=category,
            content="",
        )
        post = Post.objects.get(id=1)
        Comment.objects.create(
            id=1, owner=peter, post=post, content="First Content"
        )
        Comment.objects.create(
            id=2, owner=steve, post=post, content="Second Content"
        )

    def test_user_can_update_own_comments(self):
        self.client.login(username="peter", password="pass")
        response = self.client.put(
            "/comments/1/", {"content": "Changed Content"}
        )
        comment = Comment.objects.filter(id=1).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.content, "Changed Content")

    def test_user_cant_update_others_comments(self):
        self.client.login(username="steve", password="pass")
        response = self.client.put(
            "/comments/1/", {"content": "Changed Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_comments(self):
        self.client.login(username="peter", password="pass")
        response = self.client.delete("/comments/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_others_comments(self):
        self.client.login(username="steve", password="pass")
        response = self.client.delete("/comments/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
