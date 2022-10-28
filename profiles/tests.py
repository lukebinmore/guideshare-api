from rest_framework.test import APITestCase
from rest_framework import status
from .models import Profile
from django.contrib.auth.models import User


# Tests for the profile detail view
class ProfileDetailViewTests(APITestCase):
    def setUp(self):
        """
        Setup for following view tests
        """
        User.objects.create_user(username="peter", password="pass")
        User.objects.create_user(username="steve", password="pass")

    def test_can_retrieve_profile(self):
        response = self.client.get("/profiles/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["owner"], "peter")

    def test_users_can_update_own_profile(self):
        self.client.login(username="peter", password="pass")
        response = self.client.put("/profiles/1/", {"first_name": "peter"})
        profile = Profile.objects.get(id=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.first_name, "peter")

    def test_users_cant_update_others_profile(self):
        self.client.login(username="steve", password="pass")
        response = self.client.put("/profiles/1/", {"first_name": "peter"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_profile_disables_user(self):
        self.client.login(username="peter", password="pass")
        response = self.client.delete("/profiles/1/")
        peter = User.objects.get(username="peter")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(peter.is_active, False)

    def test_users_can_delete_own_profile(self):
        self.client.login(username="peter", password="pass")
        response = self.client.delete("/profiles/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_users_cant_delete_others_profile(self):
        self.client.login(username="steve", password="pass")
        response = self.client.delete("/profiles/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# Tests for the profile list view
class ProfileListViewTests(APITestCase):
    def setUp(self):
        """
        Setup for following view tests
        """
        User.objects.create_user(username="peter", password="pass")
        User.objects.create_user(username="steve", password="pass")
        User.objects.create_user(username="paul", password="pass")

    def test_can_list_profiles(self):
        response = self.client.get("/profiles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)

    def test_can_list_filtered_profiles(self):
        peter = Profile.objects.get(id=1)
        steve = Profile.objects.get(id=2)
        paul = Profile.objects.get(id=3)
        peter.following.add(paul)
        steve.following.add(paul)
        response = self.client.get("/profiles/?following=3")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)


# Tests for the saved following view
class SavedFollowingViewTests(APITestCase):
    def setUp(self):
        """
        Setup for following view tests
        """
        User.objects.create_user(username="peter", password="pass")
        User.objects.create_user(username="steve", password="pass")
        User.objects.create_user(username="paul", password="pass")
        peter = Profile.objects.get(id=1)
        steve = Profile.objects.get(id=2)
        paul = Profile.objects.get(id=3)
        peter.following.add(paul)
        peter.following.add(steve)

    def test_can_retrieve_saved_following(self):
        response = self.client.get("/saved-following/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["following"], [3, 2])

    def test_users_can_update_own_saved_following(self):
        self.client.login(username="peter", password="pass")
        response = self.client.put("/saved-following/1/", {"following": [2]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_cant_update_others_saved_following(self):
        self.client.login(username="steve", password="pass")
        response = self.client.put("/saved-following/1/", {"following": [2]})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
