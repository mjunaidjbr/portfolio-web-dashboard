from django.shortcuts import render

# Create your views here.
def portfolio_site(request):
    return render(request, 'portfolio_catalog/portfolio.html')
       