from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Incident
from .forms import IncidentForm

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