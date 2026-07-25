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

# Doit correspondre à la date affichée dans la vue (date_fin_iso)
DATE_CIBLE = datetime(2026, 7, 25, 2, 56, 00)

REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

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


def generer_pdf() -> None:
    """Régénère le PDF à partir de l'état actuel des emails collectés.
    Écrase le PDF précédent s'il existe déjà (pour inclure les nouveaux
    emails ajoutés depuis la dernière génération)."""
    emails = lire_emails_dechiffres()
    if not emails:
        logger.info("Aucun email collecté, rien à générer.")
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