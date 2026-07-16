from django import forms
from allauth.account.forms import SignupForm
from .models import User, UserProfile
from .choices import UserRole


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "w-full px-4 py-2 border border-slate-200 rounded-lg", "placeholder": "••••••••"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "w-full px-4 py-2 border border-slate-200 rounded-lg", "placeholder": "••••••••"}),
    )

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "role", "state", "lga"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "w-full px-4 py-2 border border-slate-200 rounded-lg"})
        self.fields["email"].widget.attrs.update({"placeholder": "user@example.com"})
        self.fields["username"].widget.attrs.update({"placeholder": "username"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "John"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Doe"})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "John"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Doe"}),
    )
    role = forms.ChoiceField(
        choices=UserRole.choices,
        label="Role",
        required=False,
        widget=forms.Select(),
    )
    state = forms.CharField(
        max_length=100,
        label="State",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Lagos"}),
    )
    lga = forms.CharField(
        max_length=100,
        label="LGA",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Ikeja"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "w-full px-4 py-2 border border-slate-200 rounded-lg"})
        self.fields["email"].widget.attrs.update({"placeholder": "user@example.com"})
        self.fields["username"].widget.attrs.update({"placeholder": "username"})
        self.fields["password1"].widget.attrs.update({"placeholder": "••••••••"})
        self.fields["password2"].widget.attrs.update({"placeholder": "••••••••"})

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.role = self.cleaned_data.get("role", UserRole.CITIZEN)
        user.state = self.cleaned_data.get("state")
        user.lga = self.cleaned_data.get("lga")
        user.save()
        return user