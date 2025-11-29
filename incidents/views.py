from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Views 
@login_required
def incident_list(request):
    return render(request, "incidents/incident_list.html")
