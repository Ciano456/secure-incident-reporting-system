"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: SECURE

Description:
This file contains the view functions for the secure implementation of the
incident reporting system.

Key security improvements compared to the insecure branch:
- No raw SQL queries are used; everything goes through the Django ORM.
- Access to "internal" comments is restricted to staff users only.
- Logging is more controlled and does not include full comment bodies,
  reducing the risk of sensitive data exposure in log files.
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Incident
from .forms import IncidentForm, CommentForm

# Use the dedicated 'incidents' logger configured in settings.py
logger = logging.getLogger("incidents")


@login_required
def incident_list(request):
    """
    Display a list of all incidents.

    SECURITY NOTES:
    - Uses the Django ORM exclusively (no raw SQL).
    - In contrast to the insecure branch, there is no user-controlled string
      being concatenated into queries, which prevents SQL injection via
      the list view.
    """
    incidents = (
        Incident.objects
        .all()
        .select_related("reporter")
    )

    context = {
        "incidents": incidents,
    }
    return render(request, "incidents/incident_list.html", context)


@login_required
def incident_create(request):
    """
    Handle creation of a new incident via the IncidentForm.

    - On GET: render a blank form.
    - On POST: validate input, set the reporter to the logged-in user,
      save the incident via the ORM, and log the event.
    - Logging records high-level metadata (user, incident ID, severity,
      category) without storing sensitive content in the log file.
    """
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reporter = request.user
            incident.save()

            logger.info(
                "Incident created",
                extra={
                    "user": request.user.username,
                    "incident_id": incident.id,
                    "severity": incident.severity,
                    "category": incident.category,
                },
            )

            return redirect("incidents:list")
    else:
        form = IncidentForm()

    return render(request, "incidents/incident_form.html", {"form": form})


@login_required
def incident_detail(request, pk):
    """
    Display a single incident and allow authenticated users to add comments.

    SECURITY NOTES:
    - Only staff users are allowed to mark comments as "internal".
    - Non-staff users always have is_internal forced to False.
    - When rendering, staff users can see both internal and external comments,
      but non-staff users only see non-internal comments.
    - Logging records that a comment was added without storing the full text
      of the comment body, reducing the risk of sensitive data exposure
      in application logs.
    """
    incident = get_object_or_404(
        Incident.objects.select_related("reporter"),
        pk=pk,
    )

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.incident = incident
            comment.author = request.user

            # Enforce access control on internal comments:
            # Only staff members can create internal comments.
            if not request.user.is_staff:
                comment.is_internal = False

            comment.save()

            logger.info(
                "Comment added to incident",
                extra={
                    "user": request.user.username,
                    "incident_id": incident.id,
                    "is_internal": comment.is_internal,
                },
            )

            return redirect("incidents:detail", pk=incident.pk)
    else:
        form = CommentForm()

    # Staff users see all comments; normal users only see non-internal ones.
    if request.user.is_staff:
        comments = incident.comments.all()
    else:
        comments = incident.comments.filter(is_internal=False)

    context = {
        "incident": incident,
        "comments": comments,
        "form": form,
    }
    return render(request, "incidents/incident_detail.html", context)