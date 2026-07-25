from django.shortcuts import render
from datetime import datetime
from django.utils import timezone

# Create your views here.
def index(request):

    # definission de la date cible en python (Année, Mois, Jour, Heure, Minute, Seconde)

    date_time =  datetime(2026, 8, 31, 23, 59, 59)

    #  On envoie la date au format ISO (ex: "2027-12-31T23:59:59")
    context = {
        'date_fin_iso': date_time.isoformat(),
      
    }
    return render(request, 'index.html', context)


