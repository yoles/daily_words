from typing import Tuple

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.models import User
from users.token import account_activation_token


class EmailSelector:
    @staticmethod
    def get_account_activation_message(user: User, domain: str, debug=False) -> Tuple[str, str]:
        subject = '[DailyWords] Activation de votre compte'
        file_name = "activation_account_email.html"
        if debug:
            file_name = f"debug_{file_name}"
        template_url = f"users/emails/{file_name}"
        message = render_to_string(template_url, {
            'user': user,
            'domain': domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        return subject, message
