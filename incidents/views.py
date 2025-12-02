"""
Student Name: Cian O'Connor
Student Number: 22109668
Student Email: x22109668@student.ncirl.ie
Project: Secure Incident Reporting System
Branch: INSECURE

Description:
View functions for the incident reporting application.

This version is intentionally insecure so that common web vulnerabilities
can be demonstrated and tested, including:

- SQL injection (raw query in incident_list)
- Weak access control around "internal" comments
- Overly verbose logging that may leak sensitive data
"""

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Incident
from .forms import IncidentForm, CommentForm

# Use the named logger defined in settings.py so messages go to app.log
logger = logging.getLogger("incidents")


@login_required
def incident_list(request):
    """
    List all incidents for the logged-in user.

    INSECURE BEHAVIOUR (for teaching purposes):
    - If a search term 'q' is provided, it is concatenated directly into a
      raw SQL string with no parameterisation.
    - This makes the query vulnerable to SQL injection and is used in the
      report to show how ZAP and manual testing can detect it.
    """
    q = request.GET.get("q")

    if q:
        # Deliberately vulnerable search logic
        # Any characters entered by the user are dropped directly into the SQL.
        # Example of a dangerous input:
        #   ' OR 1=1 --
        raw_sql = f"""
            SELECT * FROM incidents_incident
            WHERE title LIKE '%{q}%' OR description LIKE '%{q}%'
            ORDER BY created_at DESC
        """
        incidents = Incident.objects.raw(raw_sql)
    else:
        incidents = (
            Incident.objects
            .all()
            .select_related("reporter")
        )

    context = {
        "incidents": incidents,
        "search_term": q or "",
    }
    return render(request, "incidents/incident_list.html", context)


@login_required
def incident_create(request):
    """
    Handle the 'Report new incident' form.

    - On GET: display an empty IncidentForm.
    - On POST: validate the form, attach the current user as reporter,
      save the incident, and write a log entry.
    """
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reporter = request.user
            incident.save()

            # Log that a new incident was created (for audit trail)
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
    Show a single incident and allow comments to be added.

    INSECURE BEHAVIOUR (for teaching purposes):
    - Any logged-in user can mark a comment as "internal".
      In the secure version, only staff should be able to do this.
    - All comments (including internal ones) are shown to every user.
    - The log entry includes the full comment body, which can result in
      sensitive data being written to logs.
    """
    # Fetch the incident and its reporter or return 404 if not found
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

            # INSECURE: no restriction on who can set is_internal.
            # In the secure branch, non-staff users are forced to is_internal=False.
            comment.save()

            # INSECURE: logging full comment body may leak sensitive data.
            logger.info(
                f"Comment added to incident (insecure) | user={request.user.username} "
                f"| incident_id={incident.id} | is_internal={comment.is_internal} "
                f"| body={comment.body}"
            )

            return redirect("incidents:detail", pk=incident.pk)
    else:
        form = CommentForm()

    # INSECURE: internal comments are not filtered out,
    # so every logged-in user can see them.
    comments = incident.comments.all()

    context = {
        "incident": incident,
        "comments": comments,
        "form": form,
    }
    return render(request, "incidents/incident_detail.html", context)