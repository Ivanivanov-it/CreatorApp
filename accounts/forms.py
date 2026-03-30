from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import CustomUser
from common.validators import ValidatedCloudinaryFileField

UserModel = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username']



    def clean_username(self):
        username = self.cleaned_data['username']
        if UserModel.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['email']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "email": "Email address (e.g. Ivan@gmail.com)",
        }
        for field, text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs["placeholder"] = text

class FullNameChangeForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "first_name": "First name (e.g. Ivan)",
            "last_name": "Last name (e.g. Ivanov)",
        }
        for field, text in placeholders.items():
            if field in self.fields:
                self.fields[field].widget.attrs["placeholder"] = text

class ProfilePictureChangeForm(forms.ModelForm):
    picture = ValidatedCloudinaryFileField(options={'folder': 'characters'}, required=False)

    class Meta:
        model = UserModel
        fields = ['picture']

