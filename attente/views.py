from django.contrib import messages
from django.shortcuts import redirect, render

from .emails_utils import (
    ajouter_email,
    compte_a_rebours_termine,
    generer_pdf,
    DATE_CIBLE,
)


def index(request):
    # --- Réception du formulaire de collecte d'email (méthode POST) ---
    if request.method == "POST":
        email = request.POST.get("email", "")
        try:
            ajoute = ajouter_email(email)
            if ajoute:
                messages.success(request, "Merci ! Tu seras informé(e) du lancement officiel.")
                # Si le compte à rebours est déjà terminé, on met à jour
                # immédiatement le PDF (et on l'envoie par email) pour
                # inclure ce nouvel email.
                if compte_a_rebours_termine():
                    generer_pdf()
            else:
                messages.info(request, "Cet email est déjà enregistré.")
        except ValueError:
            messages.error(request, "Email invalide, merci de vérifier ta saisie.")

        return redirect("index")  # évite le renvoi du formulaire au refresh (pattern PRG)

    # --- Si le compte à rebours est terminé, on s'assure que le PDF existe
    # et a bien été envoyé par email ---
    if compte_a_rebours_termine():
        generer_pdf()

    # --- Affichage normal de la page (méthode GET) ---
    context = {
        "date_fin_iso": DATE_CIBLE.isoformat(),
    }
    return render(request, "index.html", context)