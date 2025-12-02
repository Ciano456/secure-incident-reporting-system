"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System

File Purpose:
This file defines the configuration class for the Django "incidents" app.

Django uses this class to:
- Register the application with the framework
- Handle application-specific settings
- Ensure consistent behaviour when migrations are run
- Manage default field settings for models
"""

from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    # Sets the default type for automatically created primary keys
    default_auto_field = 'django.db.models.BigAutoField'

    # The name of the application as registered in INSTALLED_APPS
    name = 'incidents'