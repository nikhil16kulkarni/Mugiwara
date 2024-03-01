from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from .forms import UserUpdateForm, BankingUserUpdateForm
# users/views.py
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Transactions, BankingUser

from .forms import DebitForm, CreditForm
from django.shortcuts import render, redirect
from .forms import Transactions_form

from .forms import Transactions_form
from .models import Transactions


from django.shortcuts import render, get_object_or_404, redirect


from .models import Transactions


from django.db.models import Q




def home(request):
   # laptopo = LaptopO.objects.all().order_by('-laptop_id')[:12]
   # context = {
   #      'laptopo': laptopo,
   #  }
  
   return render(request, 'users/home.html')




# class UpdateBankingUserView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
#     model = BankingUser
#     form_class = BankingUserUpdateForm
#     success_message = 'Details updated successfully'
  
#     def test_func(self):
#         if self.request.user.is_authenticated:
#             return True
#         return False
  
#     def get_object(self, *args, **kwargs):
#         return BankingUser.objects.get(user = self.kwargs['pk'])


#     def get_success_url(self):
#         return reverse("profile", kwargs={"pk": self.kwargs['pk']})




@login_required
def profile(request):
   if request.method == 'POST':
       u_form = UserUpdateForm(request.POST, instance = request.user)
       b_form = BankingUserUpdateForm(request.POST, instance = request.user.bankinguser)
       if u_form.is_valid() and b_form.is_valid():
           u_form.save()
           b_form.save()
           messages.success(request, 'Profile Updated Successfully')
           return redirect('profile')
   u_form = UserUpdateForm(instance = request.user)
   b_form = BankingUserUpdateForm(instance = request.user.bankinguser)


   context = {
       'u_form': u_form,
       'b_form': b_form,
   }
   return render(request, 'users/profile.html', context)




@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = Transactions_form(request.POST)
        if form.is_valid():
            form.instance.transaction_status = 'pending'
            form.instance.transaction_handler = request.user.bankinguser
            form.save()
            return redirect('user_transactions')
    else:
        current_user_account = request.user.bankinguser.account_set.first()
        initial_data = {'from_account': current_user_account}
        form = Transactions_form(initial=initial_data)

    return render(request, 'users/create_transaction.html', {'form': form})





@login_required
def all_transactions(request):
   # Filter transactions where the current user is either the sender or the receiver
   transactions = Transactions.objects.filter(
       Q(from_account__user=request.user.bankinguser) | Q(to_account__user=request.user.bankinguser)
   ).distinct()  


   return render(request, 'users/all_transactions.html', {'transactions': transactions})




@login_required
def user_transactions(request):
   transactions = Transactions.objects.filter(
       Q(from_account__user=request.user.bankinguser) | Q(to_account__user=request.user.bankinguser)
   ).distinct()

   banking_user = request.user.bankinguser
   Account_user = Account.objects.get(user=banking_user)
   account_balance=Account_user.account_bal
   return render(request, 'users/user_transactions.html', {'transactions': transactions, 'account_balance': account_balance})


@login_required
# users/views.py
def approve_transaction(request, transaction_id):
   transaction = get_object_or_404(Transactions, id=transaction_id)


   if request.method == 'POST':
       if transaction.transaction_status == 'pending':
           # Update the transaction status to 'approved'



           # Perform deduction from "From_account"
           from_account = transaction.from_account
           from_account.account_bal -= transaction.amount
           to_account = transaction.to_account
           to_account.account_bal+=transaction.amount
           from_account.save()
           to_account.save()
           transaction.transaction_status = 'approved'

           transaction.save()


           # Perform additional actions if needed


           # Redirect or render a response as needed


   # Render a page for approving transactions (optional)
   return redirect('/user_transactions', transaction_id=transaction_id)




@login_required
def decline_transaction(request, transaction_id):
   transaction = get_object_or_404(Transactions, id=transaction_id)


   if request.method == 'POST':
       if transaction.transaction_status == 'pending':
       # Update the transaction status to 'rejected'
           transaction.transaction_status = 'rejected'
           transaction.save()


       # Redirect or render a response as needed


   # Render a page for declining transactions (optional)
   return redirect('/user_transactions', transaction_id=transaction_id)



from django.db import transaction

@transaction.atomic
def debit_view(request):
    form = DebitForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']

        user = request.user.bankinguser
        account = Account.objects.get(user=user)

        if account.account_bal < amount:
            messages.error(request, "Insufficient funds.")
            return redirect('debit_view')

        # Deduct the amount from the account balance
        account.account_bal -= amount
        account.save()

        # Create a debit transaction record
        transaction_handler = BankingUser.objects.get(user=request.user)
        Transactions.objects.create(
            from_account=account,
            to_account=account,
            amount=amount,
            transaction_status='pending',
            transaction_handler=transaction_handler,
        )
        return redirect('/user_transactions')

    return render(request, 'users/debit_template.html', {'form': form})





@transaction.atomic
def credit_view(request):
    form = CreditForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        amount = form.cleaned_data['amount']

        user = request.user.bankinguser
        account = Account.objects.get(user=user)

        # Add the amount to the account balance
        account.account_bal += amount
        account.save()

        # Create a credit transaction record
        transaction_handler = BankingUser.objects.get(user=request.user)
        Transactions.objects.create(
            from_account=account,
            to_account=account,
            amount=amount,
            transaction_status='pending',
            transaction_handler=transaction_handler,
        )


        return redirect('/user_transactions')

    return render(request, 'users/credit_template.html', {'form': form})
