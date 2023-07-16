from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import User, EmailVerification


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        data = {
            'first_name': 'testuser', 'last_name': 'testuser',
            'username': 'testuser', 'email': 'test@mail.com',
            'password1': '1234457pP#', 'password2': '1234457pP#'
        }
        username = data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, data)

        # check creating of user
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        print(email_verification.first().expiration.date())
        print((now() + timedelta(hours=48)).date())
        self.assertEquals(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует', html=True)




