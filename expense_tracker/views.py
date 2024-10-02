from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Create your views here.

@login_required(login_url=reverse_lazy('expense_tracker:login_page'))  # Use namespaced URL
def expense_tracker_dashboard(request):
    return render(request, 'expense_tracker/dashboard.html')


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