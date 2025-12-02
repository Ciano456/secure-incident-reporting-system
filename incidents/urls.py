"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: SECURE

Description:
This file defines all URL routes for the incidents application.

Each URL pattern maps an address in the browser to a corresponding
view function in views.py. These routes control how users access
incident listings, create incidents, and view individual incident details.

The secure branch does not expose any unsafe routes or debugging endpoints.
All URLs are protected by authentication checks implemented in the views.
"""

from django.urls import path
from . import views

# Namespace for reverse URL resolution
app_name = 'incidents'

urlpatterns = [
    # Homepage for incidents — lists all reports
    path('', views.incident_list, name='list'),

    # Displays form used to submit a new incident
    path('create/', views.incident_create, name='create'),

    # Displays details and comments for a single incident
    path('<int:pk>/', views.incident_detail, name='detail'),
]