from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Incident
from .forms import IncidentForm, CommentForm

import logging

from django.db import connection  

logger = logging.getLogger("incidents")


@login_required
def incident_list(request):
    """
    INSECURE VERSION (insecure branch only):
    - Uses raw SQL with unescaped user input (q) to demonstrate SQL injection.
    """
    q = request.GET.get("q")

    if q:
        # Deliberately vulnerable: user input concatenated directly into SQL string
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

            # INSECURE: allow anyone to mark internal
            # (in secure branch we forced non-staff to is_internal=False)
            comment.save()

            logger.info(
                f"Comment added to incident (insecure) | user={request.user.username} "
                f"| incident_id={incident.id} | is_internal={comment.is_internal} "
                f"| body={comment.body}"
            )

            return redirect("incidents:detail", pk=incident.pk)
    else:
        form = CommentForm()

    # INSECURE: expose all comments, including internal, to all logged-in users
    comments = incident.comments.all()

    context = {
        "incident": incident,
        "comments": comments,
        "form": form,
    }
    return render(request, "incidents/incident_detail.html", context)