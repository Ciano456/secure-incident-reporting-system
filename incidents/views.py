from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Incident

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