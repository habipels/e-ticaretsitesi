from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ' Email'}),
        label="Email")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Parola'}))


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ' Username'}),
        label="Email")
    email_address = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': ' Email'}),
        label="Email")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': ' Parola'}),
        label="Parola")
    confirm = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': ' Parola'}),
        label="Parola")

    def clean(self):
        username = self.cleaned_data.get("username")
        email_address = self.cleaned_data.get("email_address")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")

        values = {
            "username" : username,
            "password" : password,
            "email_address":email_address
        }
        return values

