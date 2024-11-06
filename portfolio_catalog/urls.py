from django.urls import path
from . import views

app_name = "portfolio_catalog"


urlpatterns = [
    path('',views.portfolio_site, name="portfolio_site"),

]