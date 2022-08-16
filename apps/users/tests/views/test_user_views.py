from http import HTTPStatus

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from users.factories import UserFactory
from users.token import account_activation_token

REGISTER_USER_URL = reverse("users:signup")


class RegisterAccountViewTests(TestCase):

    def test_register_account_get_page(self):
        response = self.client.get(REGISTER_USER_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_register_account(self):
        payload = {
            "email": "test2@example.fr",
            "password1": "test12!",
            "password2": "test12!"
        }
        response = self.client.post(REGISTER_USER_URL, data=payload)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_register_account_no_email(self):
        payload = {
            "phone": "0123456789",
            "password1": "test",
            "password2": "wrong"
        }
        response = self.client.post(REGISTER_USER_URL, data=payload)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        errors = response.context.get('form')._errors
        error = errors["email"][0]
        self.assertEqual(error, "Ce champ est obligatoire.")

    def test_register_account_email_exists(self):
        UserFactory(email="exist@example.fr")
        payload = {
            "email": "exist@example.fr",
            "password1": "test",
            "password2": "wrong"
        }
        response = self.client.post(REGISTER_USER_URL, data=payload)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        errors = response.context.get('form')._errors
        error = errors["email"][0]
        self.assertEqual(error, _("This email already exists."))

    def test_register_account_wrong_password(self):
        payload = {
            "email": "test2@example.fr",
            "password1": "test",
            "password2": "wrong"
        }
        response = self.client.post(REGISTER_USER_URL, data=payload)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        errors = response.context.get('form')._errors
        error = errors["password2"][0]
        self.assertEqual(error, "Les deux mots de passe ne correspondent pas.")

    def test_register_account_too_common(self):
        payload = {
            "email": "test2@example.fr",
            "password1": "test",
            "password2": "test"
        }
        response = self.client.post(REGISTER_USER_URL, data=payload)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        errors = response.context.get('form')._errors
        error = errors["password2"][0]
        self.assertEqual(error, "Ce mot de passe est trop courant.")

    def test_register_account_phone_exists(self):
        UserFactory(phone="0123456789")
        payload = {
            "email": "test2@example.fr",
            "phone": "0123456789",
            "password1": "test12!",
            "password2": "test12!"
        }
        response = self.client.post(REGISTER_USER_URL, data=payload)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        errors = response.context.get('form')._errors
        print("Errors: ", errors)
        error = errors["phone"][0]
        self.assertEqual(error, _("This phone number already exists."))


class ActivateAccountViewTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_activate_account(self):
        encoding_user_id = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = account_activation_token.make_token(self.user)
        self.assertFalse(self.user.is_confirm)

        response = self.client.get(reverse(
            "users:activate-account",
            kwargs={"uidb64": encoding_user_id, "token": token}
        ), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_confirm)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your account is successfully confirmed. You can connect now.')

    def test_activate_account_wrong_uidb64(self):
        encoding_user_id = force_bytes(self.user.pk)
        token = account_activation_token.make_token(self.user)
        self.assertFalse(self.user.is_confirm)

        response = self.client.get(reverse(
            "users:activate-account",
            kwargs={"uidb64": encoding_user_id, "token": token}
        ), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'This confirmation link is not valid or expired.')
        self.assertFalse(self.user.is_confirm)
