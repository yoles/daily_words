from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['email', 'phone', 'password1', 'password2']
