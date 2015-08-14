from django import forms


class LoginForm(forms.Form):
    u_name = forms.CharField(label="Nom d'utilisateur", max_length=20)
    u_passwd = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
