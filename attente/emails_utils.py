"""
Logique de collecte d'emails chiffrés — à importer dans les vues Django.
Dépendances : pip install cryptography reportlab
"""

import hashlib
import logging
import re
from datetime import datetime
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from cryptography.fernet import Fernet, InvalidToken
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

# Les fichiers sont stockés dans un dossier dédié sous BASE_DIR, pour ne pas
# les mélanger avec le code source ni les exposer publiquement.
DOSSIER = Path(settings.BASE_DIR) / "data_emails"
DOSSIER.mkdir(exist_ok=True)

FICHIER_CLE = DOSSIER / "cle_secrete.key"
FICHIER_EMAILS = DOSSIER / "emails_chiffres.txt"
FICHIER_HASHES = DOSSIER / "emails_hashes.txt"
FICHIER_PDF = DOSSIER / "emails_finaux.pdf"
FICHIER_MARQUEUR_ENVOI = DOSSIER / "dernier_envoi.marqueur"  # évite les envois en double

# Doit correspondre à la date affichée dans la vue (date_fin_iso)
DATE_CIBLE = datetime(2026, 8, 31, 23, 59, 59)

# Adresse qui recevra le PDF final par email
EMAIL_DESTINATAIRE = "newsletters@pythonci.org"

# URL du site, utilisée dans le lien de l'email de confirmation
URL_SITE = "https://www.linkedin.com/company/pythonci/" #a changé

REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+\Z")

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# 1. Clé de chiffrement
# --------------------------------------------------------------------------

@lru_cache(maxsize=1)
def obtenir_fernet() -> Fernet:
    if FICHIER_CLE.exists():
        cle = FICHIER_CLE.read_bytes()
    else:
        cle = Fernet.generate_key()
        FICHIER_CLE.write_bytes(cle)
        logger.info("Nouvelle clé de chiffrement générée : %s", FICHIER_CLE)

    return Fernet(cle)


# --------------------------------------------------------------------------
# 2. Validation, déduplication, ajout
# --------------------------------------------------------------------------

def valider_email(email: str) -> str:
    email = email.strip().lower()
    if not REGEX_EMAIL.match(email):
        raise ValueError(f"Email invalide : {email!r}")
    return email


def email_deja_present(email: str) -> bool:
    if not FICHIER_HASHES.exists():
        return False
    empreinte = hashlib.sha256(email.encode("utf-8")).hexdigest()
    return empreinte in FICHIER_HASHES.read_text(encoding="utf-8").splitlines()


def envoyer_confirmation_utilisateur(email: str) -> bool:
    """
    Envoie un email de confirmation automatique à la personne qui vient
    de s'inscrire. Version HTML + texte brut (meilleure délivrabilité
    qu'un email 100% texte brut). Renvoie True si l'envoi a réussi,
    False sinon (sans jamais faire planter le reste du site en cas
    d'échec).
    """
    sujet = "PyCon Côte d'Ivoire 2027 — Inscription confirmée"

    texte_brut = (
        "Merci pour ton inscription à la liste d'attente de la "
        "PyCon Côte d'Ivoire 2027 !\n\n"
        "Tu seras informé(e) dès l'ouverture officielle du site.\n\n"
        "En attendant, n'hésite pas à nous suivre sur nos différents "
        "canaux pour ne manquer aucune information.\n\n"
        f"{URL_SITE}\n\n"
        "À très vite,\nL'équipe PythonCI"
    )

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.5;">
        <h2 style="color: #1a1a1a;">PyCon Côte d'Ivoire 2027</h2>
        <p>Merci pour ton inscription à la liste d'attente !</p>
        <p>Tu seras informé(e) dès l'ouverture officielle du site.</p>
        <p>En attendant, n'hésite pas à nous suivre pour ne manquer
           aucune information.</p>
        <p><a href="{URL_SITE}" style="color: #2563eb;">{URL_SITE}</a></p>
        <p>À très vite,<br>L'équipe PythonCI</p>
        <hr style="border: none; border-top: 1px solid #ddd; margin: 24px 0;">
        <p style="font-size: 12px; color: #888;">
          Tu reçois cet email car tu t'es inscrit(e) sur la liste
          d'attente PyCon Côte d'Ivoire 2027 sur
          <a href="{URL_SITE}" style="color: #888;">{URL_SITE}</a>.
        </p>
      </body>
    </html>
    """

    try:
        message = EmailMultiAlternatives(
            subject=sujet,
            body=texte_brut,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )
        message.attach_alternative(html, "text/html")
        message.send(fail_silently=False)
        logger.info("Email de confirmation envoyé à %s...", email[:3])
        return True
    except Exception as e:
        logger.error("Échec de l'envoi de la confirmation à %s... : %s", email[:3], e)
        return False


def ajouter_email(email: str) -> bool:
    """Renvoie True si ajouté, False si doublon, lève ValueError si invalide."""
    email = valider_email(email)

    if email_deja_present(email):
        logger.info("Email déjà collecté, ignoré : %s...", email[:3])
        return False

    fernet = obtenir_fernet()
    token = fernet.encrypt(email.encode("utf-8")).decode("utf-8")
    empreinte = hashlib.sha256(email.encode("utf-8")).hexdigest()

    with open(FICHIER_EMAILS, "a", encoding="utf-8") as f:
        f.write(token + "\n")
    with open(FICHIER_HASHES, "a", encoding="utf-8") as f:
        f.write(empreinte + "\n")

    logger.info("Email collecté et chiffré (%s...)", token[:20])
    envoyer_confirmation_utilisateur(email)
    return True


def decrypter_email(token_chiffre: str) -> str:
    fernet = obtenir_fernet()
    return fernet.decrypt(token_chiffre.encode("utf-8")).decode("utf-8")


# --------------------------------------------------------------------------
# 3. Compte à rebours + PDF
# --------------------------------------------------------------------------

def compte_a_rebours_termine() -> bool:
    return datetime.now() >= DATE_CIBLE


def lire_emails_dechiffres() -> list[str]:
    if not FICHIER_EMAILS.exists():
        return []

    fernet = obtenir_fernet()
    resultats = []

    with open(FICHIER_EMAILS, "r", encoding="utf-8") as f:
        for numero_ligne, ligne in enumerate(f, start=1):
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                resultats.append(fernet.decrypt(ligne.encode("utf-8")).decode("utf-8"))
            except InvalidToken:
                logger.warning("Ligne %d illisible (token invalide), ignorée.", numero_ligne)

    return resultats


def envoyer_pdf_par_email() -> bool:
    """
    Envoie le PDF final par email à EMAIL_DESTINATAIRE, en pièce jointe.
    Renvoie True si l'envoi a réussi, False sinon.
    """
    if not FICHIER_PDF.exists():
        logger.warning("Envoi impossible : le PDF n'existe pas encore.")
        return False

    try:
        message = EmailMessage(
            subject="PyCon Côte d'Ivoire 2027 — Liste finale des emails collectés",
            body="Le compte à rebours est terminé. Vous trouverez en pièce jointe la liste des emails collectés.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[EMAIL_DESTINATAIRE],
        )
        message.attach_file(str(FICHIER_PDF))
        message.send(fail_silently=False)
        logger.info("PDF envoyé par email à %s", EMAIL_DESTINATAIRE)
        return True
    except Exception as e:
        logger.error("Échec de l'envoi du PDF par email : %s", e)
        return False


def generer_pdf() -> None:
    """Régénère le PDF à partir de l'état actuel des emails collectés, puis
    l'envoie automatiquement par email — mais une seule fois par nombre
    d'emails collecté (pas de renvoi si rien n'a changé depuis le dernier
    envoi)."""
    emails = lire_emails_dechiffres()
    if not emails:
        logger.info("Aucun email collecté, rien à générer.")
        return

    # Évite de renvoyer le même email en boucle à chaque visite de page :
    # on ne régénère + renvoie que si le nombre d'emails a changé depuis
    # le dernier envoi réussi.
    dernier_total_envoye = None
    if FICHIER_MARQUEUR_ENVOI.exists():
        dernier_total_envoye = FICHIER_MARQUEUR_ENVOI.read_text(encoding="utf-8").strip()

    if dernier_total_envoye == str(len(emails)):
        logger.info("PDF déjà à jour et déjà envoyé (%d emails), rien à refaire.", len(emails))
        return

    doc = SimpleDocTemplate(str(FICHIER_PDF), pagesize=A4)
    styles = getSampleStyleSheet()
    contenu = [
        Paragraph("PyCon Côte d'Ivoire 2027 — Liste des emails collectés", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]),
        Paragraph(f"Total : {len(emails)} email(s)", styles["Normal"]),
        Spacer(1, 20),
    ]
    contenu.extend(
        Paragraph(f"{i}. {email}", styles["Normal"]) for i, email in enumerate(emails, start=1)
    )

    doc.build(contenu)
    logger.info("PDF généré : %s (%d emails)", FICHIER_PDF, len(emails))

    if envoyer_pdf_par_email():
        FICHIER_MARQUEUR_ENVOI.write_text(str(len(emails)), encoding="utf-8")