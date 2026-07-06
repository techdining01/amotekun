from allauth.account.forms import SignupForm
from django import forms
from .models import User


class CustomSignupForm(SignupForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.RadioSelect,
        initial="CITIZEN",
        required=True
    )

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data["role"]
        user.save()
        return user
