from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from .emails_utils import (
    ajouter_email,
    compte_a_rebours_termine,
    generer_pdf,
    DATE_CIBLE,
    FICHIER_PDF,
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
                # immédiatement le PDF pour inclure ce nouvel email.
                if compte_a_rebours_termine():
                    generer_pdf()
            else:
                messages.info(request, "Cet email est déjà enregistré.")
        except ValueError:
            messages.error(request, "Email invalide, merci de vérifier ta saisie.")

        return redirect("index")  # évite le renvoi du formulaire au refresh (pattern PRG)

    # --- Si le compte à rebours est terminé, on s'assure que le PDF existe ---
    if compte_a_rebours_termine():
        generer_pdf()

    # --- Affichage normal de la page (méthode GET) ---
    context = {
        "date_fin_iso": DATE_CIBLE.isoformat(),
    }
    return render(request, "index.html", context)


@staff_member_required  # seul un compte admin/staff Django peut accéder à cette route
def telecharger_pdf(request):
    """
    Sert le PDF final au téléchargement. Le régénère d'abord si le compte
    à rebours est terminé, pour être sûr d'avoir la version la plus à jour.
    """
    if not compte_a_rebours_termine():
        raise Http404("Le compte à rebours n'est pas encore terminé.")

    generer_pdf()  # régénère avec les derniers emails avant de servir le fichier

    if not FICHIER_PDF.exists():
        raise Http404("Aucun email collecté, le PDF n'a pas pu être généré.")

    return FileResponse(
        open(FICHIER_PDF, "rb"),
        as_attachment=True,
        filename="emails_pyconci2027.pdf",
    )