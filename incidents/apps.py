"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
This file defines configuration settings for the incidents Django app.
It tells Django how the application should be loaded and identifies
the app within the overall project structure.
"""

from django.apps import AppConfig


class IncidentsConfig(AppConfig):
    """
    Application configuration for the incidents app.

    This class allows Django to recognise the app and apply default
    behaviours such as primary key handling.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'incidents'