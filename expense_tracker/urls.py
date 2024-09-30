from django.urls import path
from . import views

app_name = "expense_tracker"


urlpatterns = [
    path('',views.expense_tracker_dashboard, name="expense_dashboard"),
]