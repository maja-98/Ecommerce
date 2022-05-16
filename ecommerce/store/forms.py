from django.contrib.auth.forms import UserCreationForm
from .models import Customer,User
from django.forms import ModelForm

class CustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2']