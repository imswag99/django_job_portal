# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "role", "password1", "password2")

    def clean_role(self):
        role = self.cleaned_data.get("role")
        # Prevent users from registering as admin manually
        if role == User.ADMIN:
            raise forms.ValidationError("You cannot register as an admin.")
        return role


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "role")


from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()