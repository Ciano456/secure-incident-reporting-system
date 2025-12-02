"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
This file defines all URL routes related to the incident reporting feature.
Each route maps a web URL to a specific Django view function that controls
what logic is run when a user accesses that page.
"""

from django.urls import path
from . import views

# name for this Django app so URLs can be referenced safely elsewhere
app_name = 'incidents'

urlpatterns = [
    # Shows all incidents (searchable in the insecure version using raw SQL)
    path('', views.incident_list, name='list'),

    # Displays the form used to submit a new incident
    path('create/', views.incident_create, name='create'),

    # Displays a single incident and its comments by primary key (ID)
    path('<int:pk>/', views.incident_detail, name='detail'),
]