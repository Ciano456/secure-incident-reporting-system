from django.shortcuts import render
from django.shortcuts import render

# Views 

def incident_list(request):
    return render(request, "incidents/incident_list.html")
