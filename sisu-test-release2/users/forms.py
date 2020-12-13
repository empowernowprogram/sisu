# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
        
    
    def __init__(self, *args, **kwargs):
      super(CustomUserCreationForm, self).__init__(*args, **kwargs)

      self.fields['username'].widget.attrs['class'] = 'input'
      self.fields['password1'].widget.attrs['class'] = 'input'
      self.fields['password2'].widget.attrs['class'] = 'input'
      self.fields['email'].widget.attrs['class'] = 'input'

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=255)

