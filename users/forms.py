from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *


class UserRegistrationForm(UserCreationForm):
    user_approval = {
       'pending': 'Waiting for approval',
       'rejected': 'Rejected',
       'approved': 'Approved'
    }

    User_types = {
        'eu_cust': 'Customer',
        'eu_mo': 'Merchant/Organization',
        'iu_re': 'Employee',
        'iu_sm': 'System Manager',
        'iu_sa': 'System Administrator',
    }

    email = forms.EmailField()
    user_type = forms.ChoiceField(choices = User_types)
    user_approval = forms.ChoiceField(choices = user_approval)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'user_type']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_approval'] = forms.CharField(initial='pending', widget=forms.HiddenInput())

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', ]
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['username'].disabled = True

class BankingUserUpdateForm(ModelForm):
    class Meta:
        model = BankingUser
        fields = "__all__"
        exclude = ['user', 'user_handler', 'pd_modification_status']
        
    def __init__(self, *args, **kwargs):
        super(BankingUserUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.id:
            self.fields['user_type'].disabled = True
            
    
class AccountUpdateForm(ModelForm):
    class Meta:
        model = Account
        fields = ['account_number', 'account_type', 'account_bal', 'account_status']
        # fields = '__all__'
        # exclude = ['user', 'closed_on']
    
<<<<<<< HEAD
    def __init__(self, *args, **kwargs):
        super(AccountUpdateForm, self).__init__(*args, **kwargs)

        if self.instance.account_number:
            self.fields['account_type'].disabled = True
            self.fields['account_bal'].disabled = True
            self.fields['account_status'].disabled = True

=======
    
from django import forms
from .models import Transactions
>>>>>>> main

class Transactions_form(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['from_account', 'to_account', 'amount']

    def __init__(self, *args, **kwargs):
        super(Transactions_form, self).__init__(*args, **kwargs)

        # Remove the drop-down in the 'from_account' field
        self.fields['from_account'].widget = forms.HiddenInput()

        # Exclude the current user from the 'to_account' choices
        current_user_account = kwargs.get('initial', {}).get('from_account')
        if current_user_account:
            self.fields['to_account'].queryset = self.fields['to_account'].queryset.exclude(pk=current_user_account.pk)


class DebitForm(forms.Form):
    amount = forms.IntegerField(
        label='Amount',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter debit amount'}),
    )


class CreditForm(forms.Form):
    amount = forms.IntegerField(
        label='Amount',
        min_value=1,
        widget=forms.NumberInput(attrs={'placeholder': 'Enter credit amount'}),
    )



class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ['amount']
