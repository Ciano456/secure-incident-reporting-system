from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Incident
from .forms import IncidentForm, CommentForm

# Views 
@login_required
def incident_list(request):
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
    if request.method == "POST":
        form = IncidentForm(request.POST)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.reporter = request.user          # secure
            # status uses default 
            incident.save()
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

            # Only allow staff to mark comments as internal
            if not request.user.is_staff:
                comment.is_internal = False

            comment.save()
            return redirect("incidents:detail", pk=incident.pk)
    else:
        form = CommentForm()

    # Show internal comments only to staff
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