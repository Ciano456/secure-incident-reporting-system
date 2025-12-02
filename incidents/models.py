"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
This file defines the database models used by the incident reporting system.
It contains the structure of the database tables and their relationships.

In the insecure version, the data model is kept simple and does not enforce
additional restrictions (such as role-based access or data isolation),
allowing security issues to be demonstrated at the application level.
"""

from django.db import models
from django.contrib.auth import get_user_model

# Retrieve Django's built-in user model
User = get_user_model()


class Incident(models.Model):
    """
    Represents a single reported incident in the system.
    """

    # Severity levels used for classification
    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MED", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRIT", "Critical"

    # Status values describing an incident’s lifecycle
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "INPR", "In progress"
        RESOLVED = "RES", "Resolved"
        CLOSED = "CLOSED", "Closed"

    # Categories representing incident type
    class Category(models.TextChoices):
        IT = "IT", "IT / Security"
        SAFETY = "SAFETY", "Health & Safety"
        HR = "HR", "HR / Conduct"
        DATA = "DATA", "Data Protection"
        OTHER = "OTHER", "Other"

    # Basic incident information
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Classification fields
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

    # Relationship to the user who submitted the incident
    reporter = models.ForeignKey(
        User,
        related_name="reported_incidents",
        on_delete=models.CASCADE,
    )

    # Allows optional anonymous submission
    is_anonymous = models.BooleanField(default=False)

    # Automatically managed timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Default ordering: newest incidents appear first
    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        User friendly text display in the Django admin panel and shell.
        """
        return f"{self.title} ({self.get_severity_display()})"


class Comment(models.Model):
    """
    Represents comments added to incidents.
    Used for collaboration and internal chats.
    """

    # Link comment to incident
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

    # Main comment content (vulnerable to stored XSS in insecure branch)
    body = models.TextField()

    # Marks comment as internal-only (not enforced in insecure branch)
    is_internal = models.BooleanField(default=False)

    # Automatically record time posted
    created_at = models.DateTimeField(auto_now_add=True)

    # Comments shown in order posted
    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.incident}"