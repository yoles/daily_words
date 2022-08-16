from django.contrib.sites.shortcuts import get_current_site
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from emails.selectors import EmailSelector
from users.factories import UserFactory


class EmailSelectorTests(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_account_activation_message(self):
        domain = "localhost:8000"
        subject, message = EmailSelector.get_account_activation_message(self.user, domain, debug=False)

        self.assertEqual(subject, "[DailyWords] Activation de votre compte")
        encode_user_id = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.assertEqual(encode_user_id, "MQ")
        self.assertIn('<img src="/static/images/icons/daily_word.png" alt="Daily words logo" />', message)
        self.assertIn(f"http://{domain}/user/activate/{encode_user_id}/", message)

    def test_get_account_activation_message_debug(self):
        domain = "localhost:8000"
        subject, message = EmailSelector.get_account_activation_message(self.user, domain, debug=True)
        self.assertEqual(subject, "[DailyWords] Activation de votre compte")
        encode_user_id = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.assertEqual(encode_user_id, "MQ")
        self.assertIn(f"http://{domain}/user/activate/{encode_user_id}/", message)

