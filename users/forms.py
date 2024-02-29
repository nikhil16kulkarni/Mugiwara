from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', ]

class BankingUserUpdateForm(ModelForm):
    class Meta:
        model = BankingUser
        fields = "__all__"
        

    
    

