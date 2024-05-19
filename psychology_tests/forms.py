from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField(label='受信者のメールアドレス')
    message = forms.CharField(widget=forms.Textarea, label='メッセージ')

# from django.contrib.auth.forms import AuthenticationForm

# class EmailForm(AuthenticationForm):
#     username = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
#     remember = forms.BooleanField(label='ログイン状態を保持する', required=False)

