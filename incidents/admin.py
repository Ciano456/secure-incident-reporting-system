"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
This file registers the Incident and Comment models with the Django admin panel.

The admin interface is used for:
- Reviewing incidents
- Managing comments
- Demonstrating access to privileged system data

In the insecure version, no additional role restrictions or data protections
are implemented within the admin panel beyond Django's default authentication.
"""

from django.contrib import admin
from .models import Incident, Comment


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for incidents.
    Controls how records appear inside the Django admin dashboard.
    """

    # Columns shown in the admin list view
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

    # Filters displayed in the sidebar
    list_filter = ("category", "severity", "status", "is_anonymous", "created_at")

    # Search functionality in admin
    search_fields = ("title", "description", "reporter__username")

    # Default ordering (newest first)
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for comments.
    Used to inspect conversation history on incidents.
    """

    # Columns shown in list view
    list_display = ("id", "incident", "author", "is_internal", "created_at")

    # Filters available in admin sidebar
    list_filter = ("is_internal", "created_at")

    # Text search across comments
    search_fields = ("body", "author__username", "incident__title")

    # Most recent comments appear first
    ordering = ("-created_at",)