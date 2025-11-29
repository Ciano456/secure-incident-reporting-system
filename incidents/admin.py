from django.contrib import admin
from .models import Incident, Comment


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
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
    list_filter = ("category", "severity", "status", "is_anonymous", "created_at")
    search_fields = ("title", "description", "reporter__username")
    ordering = ("-created_at",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "incident", "author", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
    search_fields = ("body", "author__username", "incident__title")
    ordering = ("-created_at",)