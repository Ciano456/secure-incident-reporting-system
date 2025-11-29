from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Incident(models.Model):
    class Severity(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MED", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRIT", "Critical"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "INPR", "In progress"
        RESOLVED = "RES", "Resolved"
        CLOSED = "CLOSED", "Closed"

    class Category(models.TextChoices):
        IT = "IT", "IT / Security"
        SAFETY = "SAFETY", "Health & Safety"
        HR = "HR", "HR / Conduct"
        DATA = "DATA", "Data Protection"
        OTHER = "OTHER", "Other"

    title = models.CharField(max_length=200)
    description = models.TextField()

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

    reporter = models.ForeignKey(
        User,
        related_name="reported_incidents",
        on_delete=models.CASCADE,
    )
    is_anonymous = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.get_severity_display()})"
    

class Comment(models.Model):
    incident = models.ForeignKey(
        Incident,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name="incident_comments",
        on_delete=models.CASCADE,
    )
    body = models.TextField()
    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author} on {self.incident}"