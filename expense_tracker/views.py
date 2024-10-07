from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import PaymentMethodForm, FundsTransactionForm, ExpenseForm  # Import your form here
from .models import PaymentMethod, FundsTransaction, Expense
from django.db.models import Sum

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import PaymentMethodForm
from .models import PaymentMethod

# @login_required(login_url=reverse_lazy('expense_tracker:login_page'))
# def expense_tracker_dashboard(request):
#     if request.method == "POST":
#         submit_form_value = request.POST.get('submit_form')
#         if submit_form_value == 'payment_form':
#             form1 = PaymentMethodForm(request.POST)
#             if form1.is_valid():
#                 # Check if the payment method with the same name already exists for the user
#                 existing_method = PaymentMethod.objects.filter(
#                     user=request.user,
#                     method_name=form1.cleaned_data['method_name']
#                 ).exists()

#                 if existing_method:
#                     # Add an error message to the form
#                     form1.add_error('method_name', 'Payment method with this name already exists.')
#                 else:
#                     # Save the form
#                     payment_method = form1.save(commit=False)
#                     payment_method.user = request.user  # Assign the current user
#                     payment_method.save()
#                     messages.success(request, 'Payment method created successfully!')
#                     return redirect('expense_tracker:expense_dashboard')
#             else:
#                 messages.error(request, 'Please correct the errors below.')
#         else:
#             form1 = PaymentMethodForm()
#     else:
#         form1 = PaymentMethodForm()

#     # Fetch payment methods with both method_name and id
#     user_payment_methods = PaymentMethod.objects.filter(user=request.user)

#     return render(request, 'expense_tracker/dashboard.html', {
#         'username': request.user,
#         'form1': form1,
#         'payment_methods': user_payment_methods,  # Pass the list of payment method names
#     })



@login_required(login_url='expense_tracker:login_page')  # Adjust URL as needed
def expense_tracker_dashboard(request):
    form1 = PaymentMethodForm()
    form2 = FundsTransactionForm()  # Initialize form2 for GET requests
    form3 = ExpenseForm()  # Assuming this is the form handling the expense addition

    if request.method == "POST":
        submit_form_value = request.POST.get('submit_form')

        if submit_form_value == 'payment_form':
            # Handling Payment Method Form
            form1 = PaymentMethodForm(request.POST)
            if form1.is_valid():
                existing_method = PaymentMethod.objects.filter(
                    user=request.user,
                    method_name=form1.cleaned_data['method_name']
                ).exists()

                if existing_method:
                    form1.add_error('method_name', 'Payment method with this name already exists.')
                else:
                    payment_method = form1.save(commit=False)
                    payment_method.user = request.user
                    payment_method.save()
                    # Create a FundsTransaction with 0 value for the new payment method
                    init_bank = FundsTransaction(
                        payment_method=payment_method,
                        amount=0.00,  # Set initial funds to 0
                        source_details="Initial balance"  # Optional: add details about the source
                    )
                    init_bank.save()  # Save the FundsTransaction

                    messages.success(request, 'Payment method created successfully with initial funds of 0.')
                    return redirect('expense_tracker:expense_dashboard')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif submit_form_value == 'funds_form':
            # Handling Funds Transaction Form
            form2 = FundsTransactionForm(request.POST)

            if form2.is_valid():
                # Get selected payment method by its ID
                payment_method_id = request.POST.get('funds_account')
                try:
                    # Attempt to retrieve the payment method
                    payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)

                    # Save the funds transaction
                    funds_transaction = form2.save(commit=False)
                    funds_transaction.payment_method = payment_method  # Set the payment method
                    funds_transaction.save()  # Save the transaction

                    messages.success(request, 'Funds added successfully!')
                    return redirect('expense_tracker:expense_dashboard')
                
                except PaymentMethod.DoesNotExist:
                    # If the payment method does not exist, add an error to form2
                    form2.add_error(None, 'Please select a valid payment method.')
            else:
                # If the form is invalid, display the errors
                messages.error(request, 'Please correct the errors below.')
        
        elif submit_form_value == 'expense_form':
            # Handling Add Expense Form submission
            form3 = ExpenseForm(request.POST)
            if form3.is_valid():
                # Get selected payment method by its ID
                payment_method_id = request.POST.get('payment-method')
                try:
                    # Attempt to retrieve the payment method
                    payment_method = PaymentMethod.objects.get(id=payment_method_id, user=request.user)

                    # Save the funds transaction
                    expense = form3.save(commit=False)
                    expense.user = request.user
                    expense.payment_method = payment_method  # Set the payment method
                    expense.save()  # Save the transaction

                    messages.success(request, 'Expense added successfully!')
                    return redirect('expense_tracker:expense_dashboard')
                
                except PaymentMethod.DoesNotExist:
                    # If the payment method does not exist, add an error to form2
                    form2.add_error(None, 'Please select a valid payment method.')
            else:
                # If the form is invalid, display the errors
                messages.error(request, 'Please correct the errors below.')

    # Fetch user payment methods
    user_payment_methods = PaymentMethod.objects.filter(user=request.user)
    # Aggregate the total funds by payment method
    funds_by_payment_method = FundsTransaction.objects.filter(payment_method__user=request.user)\
        .values('payment_method__method_name')\
        .annotate(total_amount=Sum('amount'))\
        .order_by('payment_method__method_name')

    # Convert the result to a dictionary
    funds_dict = {item['payment_method__method_name']:float(item['total_amount']) for item in funds_by_payment_method}

    # Aggregate the total expenses by payment method
    expenses_by_payment_method = Expense.objects.filter(payment_method__user=request.user)\
        .values('payment_method__method_name')\
        .annotate(total_expense=Sum('amount'))\
        .order_by('payment_method__method_name')

    # Convert expenses to a dictionary for quick lookup
    expenses_dict = {item['payment_method__method_name']: float(item['total_expense']) for item in expenses_by_payment_method}

    # Create the final funds-expense dictionary
    funds_expense_dict = {}
    for item in funds_by_payment_method:
        method_name = item['payment_method__method_name']
        total_funds = float(item['total_amount'])
        total_expense = expenses_dict.get(method_name, 0)  # Get expenses or 0 if not found
        remaining_funds = total_funds - total_expense
        funds_expense_dict[method_name] = remaining_funds

    return render(request, 'expense_tracker/dashboard.html', {
        'username': request.user,
        'form1': form1,
        'form2': form2,  # Include form2 in the context,
        'form3': form3,  # Include form3 in the context
        'payment_methods': user_payment_methods,
        'funds_summary': funds_expense_dict,  # Pass the funds dictionary to the context
    })



@login_required(login_url=reverse_lazy('expense_tracker:login_page'))
def delete_payment_method(request):
    if request.method == "POST":
        method_id = request.POST.get('method_id')
        try:
            # Ensure the user is deleting their own payment method
            payment_method = PaymentMethod.objects.get(id=method_id, user=request.user)
            payment_method.delete()
            messages.success(request, 'Payment method removed successfully!')
        except PaymentMethod.DoesNotExist:
            messages.error(request, 'Payment method not found or you do not have permission to delete it.')

    return redirect('expense_tracker:expense_dashboard')

# @login_required(login_url=reverse_lazy('expense_tracker:login_page'))  # Use namespaced URL
# def expense_tracker_dashboard(request):
#     if request.method == "POST":
#         print(request.POST)
#     return render(request, 'expense_tracker/dashboard.html',context={ 'username': request.user})

# @login_required(login_url=reverse_lazy('expense_tracker:login_page'))
# def expense_tracker_dashboard(request):
#     if request.method == "POST":
#         method_name = request.POST.get('method_name')
#         method_type = request.POST.get('method_type')
#         additional_details = request.POST.get('additional_details')
        
#         # Check if payment method already exists
#         if PaymentMethod.objects.filter(method_name=method_name, user=request.user).exists():
#             messages.error(request, 'Payment Method already exists!')
#             return render(request, 'expense_tracker/dashboard.html', context={'username': request.user})

#         # Create the PaymentMethod instance
#         payment_method = PaymentMethod(
#             method_name=method_name,
#             method_type=method_type,
#             additional_details=additional_details,
#             user=request.user  # Associate the payment method with the current user
#         )
        
#         payment_method.save()  # Save the instance to the database

#         messages.success(request, 'Payment Method created successfully!')
#         return redirect('expense_tracker:expense_dashboard')  # Redirect to the same page or another page

#     return render(request, 'expense_tracker/dashboard.html', context={'username': request.user})


# def login_page(request):
#     return render(request, 'expense_tracker/login_page.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def login_page(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('expense_tracker:expense_dashboard')  # Redirect to dashboard on successful login
                else:
                    messages.error(request, "Invalid username or password.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            form = AuthenticationForm()
        
        return render(request, 'expense_tracker/login_page.html', {'form': form})
    else:
        return redirect('expense_tracker:expense_dashboard')




from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


def logout_user(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('expense_tracker:login_page')




from django.shortcuts import render
from django.utils.dateparse import parse_date
from .models import Expense

@login_required(login_url='expense_tracker:login_page')  # Adjust URL as needed
def filter_expenses(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # print("start_date: " + start_date)
    # print("end date : " + end_date)
    # Filter expenses based on the provided date range
    expenses = Expense.objects.all()

    if start_date:
        expenses = expenses.filter(date__gte=parse_date(start_date))
    if end_date:
        expenses = expenses.filter(date__lte=parse_date(end_date))

    # Calculate total expense amount
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, 'expense_tracker/filtered_expenses.html', {
        'expenses': expenses,
        'start_date': start_date,
        'end_date': end_date,
        'total_amount': total_amount,
    })


def search_expenses(request):
    query = request.GET.get('search-input', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    # print(request.GET)
    # print("query: " + query)
    # print("start_date: " + start_date)
    # print("end date : " + end_date)
    # Filter based on the search query, and optional date range
    expenses = Expense.objects.all()

    if query:
        expenses = expenses.filter(description__icontains=query)
    
    if start_date:
        expenses = expenses.filter(date__gte=start_date)
    
    if end_date:
        expenses = expenses.filter(date__lte=end_date)
    
    # Calculate total expense amount
    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Return filtered expenses to the template
    return render(request, 'expense_tracker/filtered_expenses.html', {'expenses': expenses,'total_amount': total_amount})

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
@login_required(login_url='expense_tracker:login_page')  # Adjust URL as needed
def delete_expense(request, expense_id):
    if request.method == 'DELETE':  # Only allow DELETE requests
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()
        
        # Calculate the new total amount after deletion
        total_amount = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
        return HttpResponse(f"PKR {total_amount}")  # Return JSON response

    return HttpResponse(status=405)  # Method Not Allowed if not DELETE