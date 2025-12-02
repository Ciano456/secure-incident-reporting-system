"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: SECURE

Description:
This file defines the core data models for the Secure Incident Reporting System.

The data structure is intentionally the same as in the insecure branch so that:
- The same database schema can be used for both versions.
- The difference in security comes from how the data is accessed, displayed,
  and logged (e.g. ORM vs raw SQL, filtering internal comments, safer logging).

The two main models are:
- Incident: a single reported issue in the organisation.
- Comment: a follow-up or update linked to an incident.
"""

from django.db import models
from django.contrib.auth import get_user_model

# Use the active Django user model (supports custom user models if configured)
User = get_user_model()


class Incident(models.Model):
    """
    Represents a single reported incident.

    This model is used in both the secure and insecure implementations.
    Security decisions (e.g. who can view or comment) are enforced in the
    view layer and not directly in the model.
    """

    # Severity options used to classify how serious the incident is
    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MED", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRIT", "Critical"

    # Status values that show where the incident is in its lifecycle
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "INPR", "In progress"
        RESOLVED = "RES", "Resolved"
        CLOSED = "CLOSED", "Closed"

    # Broad categories for the type of incident
    class Category(models.TextChoices):
        IT = "IT", "IT / Security"
        SAFETY = "SAFETY", "Health & Safety"
        HR = "HR", "HR / Conduct"
        DATA = "DATA", "Data Protection"
        OTHER = "OTHER", "Other"

    # Core incident details
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Classification fields for filtering and reporting
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        default=Severity.MEDIUM,
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN,
    )

    # Link to the user who submitted the incident
    reporter = models.ForeignKey(
        User,
        related_name="reported_incidents",
        on_delete=models.CASCADE,
    )

    # Flag indicating whether the reporter chose to remain anonymous
    is_anonymous = models.BooleanField(default=False)

    # Automatically managed timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Show most recent incidents first
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Text representation used in the Django admin and shell.
        """
        return f"{self.title} ({self.get_severity_display()})"


class Comment(models.Model):
    """
    A comment or update attached to an incident.

    In the secure branch, only staff users can create internal comments,
    and internal comments are not shown to regular users. That behaviour
    is enforced in the views, not here.
    """

    # The incident this comment belongs to
    incident = models.ForeignKey(
        Incident,
        related_name="comments",
        on_delete=models.CASCADE,
    )

    # User who wrote the comment
    author = models.ForeignKey(
        User,
        related_name="incident_comments",
        on_delete=models.CASCADE,
    )

    # Main comment body text
    body = models.TextField()

    # Marks whether the comment is internal-only (hidden from normal users)
    is_internal = models.BooleanField(default=False)

    # Created timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Comments are shown oldest-to-newest to preserve conversation order
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.incident}"