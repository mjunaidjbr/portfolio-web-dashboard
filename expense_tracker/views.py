from django.shortcuts import render

# Create your views here.



def expense_tracker_dashboard(request):
    return render(request, 'expense-tracker/dashboard.html')