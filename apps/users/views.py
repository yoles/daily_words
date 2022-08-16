from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import View
from emails.selectors import EmailSelector
from users.forms import RegisterForm
from users.models import User
from users.token import account_activation_token


def verification(request, *args, **kwargs):
    return render(request, "users/account_verification.html")


class RegisterAccount(View):
    def post(self, request, *args, **kwargs):
        form = RegisterForm(self.request.POST)
        if form.is_valid():
            user = form.save()

            current_site = get_current_site(self.request)
            debug = settings.DEBUG
            subject, message = EmailSelector.get_account_activation_message(user, current_site.domain, debug)
            user.email_user(subject, '', html_message=message)
            messages.success(self.request, _('Please, check your email to confirm your account.'))
            return redirect("users:verification-account")
        return render(
            self.request,
            "users/register_form.html",
            {"form": form},
            status=400
        )

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(self.request, "users/register_form.html", {"form": form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_confirm = True
            user.save()
            login(self.request, user)
            messages.success(self.request, _('Your account is successfully confirmed. You can connect now.'))
        else:
            messages.warning(self.request, _("This confirmation link is not valid or expired."))
        return redirect("users:verification-account")
