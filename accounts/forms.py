from django import forms
from .models import Users
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='ニックネーム')
    email = forms.EmailField(label='Emailアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']
        
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("このパスワードは短すぎます。最低 8 文字以上必要です。")
        return password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    # def save(self, commit=False):
    #     user = super().save(commit=False)
    #     validate_password(self.cleaned_data['password'], user)
    #     user.set_password(self.cleaned_data['password'])
    #     user.save()
    #     return user


# class UserLoginForm(forms.Form):
#     email = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='メールアドレス:',
        widget=forms.EmailInput(attrs={'autocomplete': 'username'})
    )
    password = forms.CharField(
        label='パスワード:',
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'})
    )
    remember = forms.BooleanField(
        label='ログイン状態を保持する',
        required=False,
        widget=forms.CheckboxInput(attrs={'autocomplete': 'off'})
    )
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    _("登録されていないユーザー,またはパスワードが違います。パスワードは8文字以上です。"),
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data