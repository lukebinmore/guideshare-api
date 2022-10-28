from rest_framework.test import APITestCase
from rest_framework import status


# Tests for the comment form view
class ContactFormViewTest(APITestCase):
    def test_can_submit_valid_form(self):
        response = self.client.post(
            "/contact-form/",
            {
                "title": "Contact Form Title",
                "email": "peter@email.com",
                "reason": 1,
                "content": "Contact Form Content",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cant_submit_invalid_form(self):
        response = self.client.post(
            "/contact-form/",
            {
                "email": "peter@email.com",
                "reason": 8,
                "content": "Contact Form Content",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
