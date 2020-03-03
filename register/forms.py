"""Here we create fonctions for login and registration"""

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    """this is form for login and run session"""

    username= forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        """cleanning entrance"""

        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('logins erronés')

            
            if not user.check_password(password):
                raise forms.ValidationError('password erronés')


        return super(UserLoginForm, self).clean(*args, **kwargs)              


class UserRegisterForm(forms.ModelForm):
    """This is form for register"""

    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """We call username email and password from meta class"""

        model = User
        
        fields = ['username',
                 'email',
                 'password']

    def clean(self, *args, **kwargs):
        """We cleanning it"""

        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)

        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username)


        if email_qs.exists():

            raise forms.ValidationError(
                "email existe deja")

        elif username_qs.exists():
            raise forms.ValidationError(
                "username existe deja")
 
        return super(UserRegisterForm, self).clean(*args, **kwargs)
