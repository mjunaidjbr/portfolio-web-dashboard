from django.urls import path
from . import views

app_name = "expense_tracker"


urlpatterns = [
    path('',views.expense_tracker_dashboard, name="expense_dashboard"),
    path('login/',views.login_page, name="login_page"),
    path('logout/',views.logout_user, name="logout_page"),
    path('delete-payment-method/', views.delete_payment_method, name='delete_payment_method'),
    path('filter-expenses/', views.filter_expenses, name='filter_expenses'),
    path('search-expenses/', views.search_expenses, name='search_expenses'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    

]