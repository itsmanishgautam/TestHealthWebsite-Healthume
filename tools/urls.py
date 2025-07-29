# tools/urls.py

from django.urls import path
from . import views

app_name = 'tools'  # Add this line to define the namespace

urlpatterns = [
    path('bmi-calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('calorie-calculator/', views.calorie_calculator, name='calorie_calculator'),
    # Add other tools URLs here if any
]
