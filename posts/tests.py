from rest_framework.test import APITestCase
from rest_framework import status
from .models import Post, Category
from django.contrib.auth.models import User


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username="peter", password="pass")
        peter = User.objects.get(username="peter")
        Category.objects.create(title="Category Title")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=1,
            owner=peter,
            title="Post Title",
            category=category,
            content="First Post",
        )
        Post.objects.create(
            id=2,
            owner=peter,
            title="Second Post Title",
            category=category,
            content="Second Post",
        )

    def test_can_list_posts(self):
        response = self.client.get("/posts/")
        count = Post.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], count)

    def test_can_list_filtered_comments(self):
        peter = User.objects.get(username="peter")
        Category.objects.create(id=2, title="Second Category")
        category = Category.objects.get(id=2)
        Post.objects.create(
            id=3,
            owner=peter,
            title="Second Post Title",
            category=category,
            content="",
        )
        response = self.client.get("/posts/?category=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)


class PostDetailViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username="peter", password="pass")
        User.objects.create_user(username="steve", password="pass")
        peter = User.objects.get(username="peter")
        Category.objects.create(title="Category Title")
        category = Category.objects.get(id=1)
        Post.objects.create(
            id=1,
            owner=peter,
            title="Post Title",
            category=category,
            content="First Post",
        )

    def test_can_retrieve_post(self):
        response = self.client.get("/posts/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    def test_cant_get_post_with_invalid_id(self):
        response = self.client.get("/posts/10/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_posts(self):
        self.client.login(username="peter", password="pass")
        response = self.client.put(
            "/posts/1/",
            {
                "title": "New Post Title",
                "category": 1,
                "content": "First Post",
            },
        )
        post = Post.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.title, "New Post Title")

    def test_user_cant_update_others_posts(self):
        self.client.login(username="steve", password="pass")
        response = self.client.put(
            "/posts/1/",
            {
                "title": "New Post Title",
                "category": 1,
                "content": "First Post",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_posts(self):
        self.client.login(username="peter", password="pass")
        response = self.client.delete("/posts/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_others_posts(self):
        self.client.login(username="steve", password="pass")
        response = self.client.delete("/posts/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostCreateViewTest(APITestCase):
    def setUp(self):
        User.objects.create_user(username="peter", password="pass")
        Category.objects.create(title="Category Title")

    def test_logged_in_user_can_create_posts(self):
        self.client.login(username="peter", password="pass")
        response = self.client.post(
            "/posts/create/",
            {
                "title": "Post Title",
                "category": "1",
                "content": "Post Content",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_user_cant_create_posts(self):
        response = self.client.post(
            "/posts/create/",
            {
                "title": "Post Title",
                "category": "1",
                "content": "Post Content",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CategoryListViewTests(APITestCase):
    def setUp(self):
        Category.objects.create(title="Windows 11 Tips")
        Category.objects.create(title="Mac OSX Tips")

    def test_can_list_categories(self):
        response = self.client.get("/posts/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
