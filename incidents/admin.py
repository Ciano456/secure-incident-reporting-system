"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System

File Purpose:
This file customises how Incident and Comment records are displayed in the
Django admin panel. It allows an administrator to view, search, filter and
manage incidents and comments more efficiently through the built-in admin UI.

The admin panel is used mainly for:
- Reviewing reported incidents
- Investigating submitted comments
- Managing internal vs public information
"""

from django.contrib import admin
from .models import Incident, Comment


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """
    Controls how incidents appear in the Django admin dashboard.
    """

    # Fields displayed in the admin list view
    list_display = (
        "id",
        "title",
        "category",
        "severity",
        "status",
        "reporter",
        "is_anonymous",
        "created_at",
    )

    # Filters available on the right side of the admin interface
    list_filter = ("category", "severity", "status", "is_anonymous", "created_at")

    # Enables searching by incident title, description, and reporter username
    search_fields = ("title", "description", "reporter__username")

    # Default ordering (newest incidents at the top)
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Controls how comments are displayed in the admin interface.
    """

    # Fields shown in the comment list view
    list_display = ("id", "incident", "author", "is_internal", "created_at")

    # Filters for internal vs public comments and by date
    list_filter = ("is_internal", "created_at")

    # Enable text searching across comment content
    search_fields = ("body", "author__username", "incident__title")

    # Show latest comments first
    ordering = ("-created_at",)