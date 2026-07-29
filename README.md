<<<<<<< HEAD
# Page d'attente — PyCon Côte d'Ivoire 2027

Ce projet est une page de lancement moderne construite avec Django pour présenter la PyCon Côte d'Ivoire 2027 avant la mise en ligne du site complet. Elle affiche un compteur de temps restant et un formulaire d'inscription par e-mail.

=======
# Page d'attente PyCon CI 2027

Projet Django minimal pour une page d'attente avec compteur, collecte d'emails chiffrée et génération de rapport PDF.
>>>>>>> main

## Présentation

<<<<<<< HEAD
- Page d'accueil responsive et élégante
- Compte à rebours dynamique
- Formulaire d'inscription par email
- Collecte d'emails **chiffrée** (chiffrement réversible, aucun email stocké en clair sur le disque)
- Détection automatique des doublons (via hash SHA-256, sans jamais déchiffrer)
- Génération automatique d'un **rapport PDF** une fois le compte à rebours terminé
- **Envoi automatique du PDF par email** (Gmail SMTP) à une adresse fixe, dès qu'il est généré
- Fonctionnement **entièrement local**
- Interface stylée avec Tailwind CSS
=======
Cette application propose :
>>>>>>> main

- une page d'accueil responsive
- un compteur de compte à rebours dynamique
- un formulaire d'inscription par email
- une collecte d'emails chiffrée et immuable
- une déduplication par hash SHA-256
- un téléchargement PDF protégé pour les administrateurs

<<<<<<< HEAD
- Python
- Django
- Tailwind CSS
- HTML/CSS/JavaScript
- `cryptography` (chiffrement des emails)
- `reportlab` (génération du PDF)
- `python-dotenv` (chargement des secrets depuis `.env`)
- `certifi` / `truststore` (correction d'un bug de certificats SSL sous Windows)
=======
## Principales fonctionnalités

- Validation d'email côté serveur
- Détection des doublons sans stocker d'email en clair
- Chiffrement des emails avec `cryptography.Fernet`
- Stockage sécurisé des emails chiffrés et des hashes dans `data_emails/`
- Génération de PDF via `reportlab`
- Route admin sécurisée : `/telecharger-pdf/`

## Technologies

- Python 3
- Django 6
- SQLite
- Tailwind CSS
- JavaScript
- `cryptography`
- `reportlab`
>>>>>>> main

## Prérequis

- Python 3.10+ ou version compatible
- pip
- Node.js et npm
- Un compte Gmail avec un **mot de passe d'application** généré (voir section Configuration email)

## Installation

```bash
git clone <url-du-projet>
cd page_attente
python -m venv .venv
.venv\Scripts\activate
<<<<<<< HEAD
```

Sur Linux/macOS :

```bash
source .venv/bin/activate
```

4. Installer les dépendances Python :

```bash
pip install django cryptography reportlab python-dotenv certifi truststore
```

5. Installer les dépendances JavaScript :

```bash
npm install
```

## Configuration email (obligatoire)

Le projet envoie automatiquement un PDF par email une fois le compte à rebours terminé. Il faut configurer un compte Gmail expéditeur.

1. Active la validation en 2 étapes sur le compte Gmail utilisé : https://myaccount.google.com/security
2. Génère un mot de passe d'application : https://myaccount.google.com/apppasswords
3. Crée un fichier `.env` à la racine du projet (jamais versionné, voir `.gitignore`) :

```text
GMAIL_APP_PASSWORD=ton_mot_de_passe_application_ici
```

4. Vérifie que `settings.py` charge bien ce fichier et configure l'envoi SMTP (déjà en place dans le projet) :

```python
import truststore
truststore.inject_into_ssl()

import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
load_dotenv()

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "compte_expediteur@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

L'adresse qui **reçoit** le PDF final se configure séparément, dans `attente/emails_utils.py` (constante `EMAIL_DESTINATAIRE`).

## Lancer le projet



```bash
python manage.py runserver
```

Ouvrir l'application dans le navigateur :
=======
pip install django cryptography reportlab
npm install
```

## Exécution

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir ensuite :
>>>>>>> main

```text
http://127.0.0.1:8000/
```

## Accès administrateur PDF

La génération et le téléchargement du PDF sont réservés au staff Django.

- URL : `http://127.0.0.1:8000/telecharger-pdf/`
- Accessible uniquement après connexion d'un superuser/staff
- Le PDF est régénéré automatiquement avant chaque téléchargement si le compte à rebours est terminé

## Structure du projet

```text
page_attente/
<<<<<<< HEAD
├── attente/                  # Application Django
├── config/                    # Configuration du projet (settings.py, urls.py)
├── static/                    # Fichiers statiques CSS/JS
├── templates/                 # Templates principaux
├── data_emails/                # Données de collecte (généré automatiquement, NE PAS versionner)
│   ├── cle_secrete.key           # Clé de chiffrement — à protéger absolument
│   ├── emails_chiffres.txt       # Emails chiffrés, un par ligne
│   ├── emails_hashes.txt         # Empreintes SHA-256 (déduplication)
│   ├── emails_finaux.pdf         # Rapport final (généré après le compte à rebours)
│   └── dernier_envoi.marqueur    # Évite de renvoyer le même email plusieurs fois
├── .env                        # Secrets locaux (mot de passe Gmail) — NE PAS versionner
├── manage.py                   # Point d'entrée Django
├── package.json                # Dépendances frontend
└── .gitignore
=======
├── attente/
│   ├── emails_utils.py      # chiffrement, déduplication, PDF
│   ├── templates/index.html # page d'accueil
│   ├── urls.py              # routes de l'application
│   └── views.py             # contrôleurs et logique de réponse
├── config/
│   ├── settings.py
│   └── urls.py
├── data_emails/             # stockage des clés, emails chiffrés et PDF
├── static/
├── db.sqlite3
├── manage.py
└── package.json
>>>>>>> main
```

## Comment fonctionne la collecte d'emails

<<<<<<< HEAD
1. Chaque email soumis via le formulaire est validé (format), puis vérifié pour éviter les doublons (comparaison de hash SHA-256, sans jamais déchiffrer les emails existants).
2. un mail de confirmation est ensuite envoyer a l'email soumis 
2. L'email est ensuite chiffré (chiffrement symétrique réversible) avant d'être écrit dans `emails_chiffres.txt`. Le fichier texte ne contient donc jamais d'email lisible.
3. La clé de chiffrement (`cle_secrete.key`) est générée automatiquement au premier email collecté, et réutilisée ensuite. **Sans cette clé, les emails sont définitivement illisibles.**
4. Une fois la date cible du compte à rebours atteinte (`DATE_CIBLE` dans `emails_utils.py`), le PDF final est généré à partir des emails déchiffrés, puis **envoyé automatiquement par email** à `EMAIL_DESTINATAIRE`.
5. Un fichier marqueur évite de renvoyer le même email à chaque visite de page : le PDF n'est régénéré et renvoyé que si le nombre d'emails collectés a changé depuis le dernier envoi réussi.
=======
1. L'utilisateur soumet un email via le formulaire.
2. Le backend valide le format et normalise l'email.
3. Le hash SHA-256 est généré et comparé aux hashes existants.
4. Si l'email est nouveau, il est chiffré et sauvegardé.
5. un mail de confirmation est envoyer a l'email de l'utilisateur
5. Les hash sont stockés pour empêcher les doublons.
6. Lorsque la date cible est dépassée, le PDF peut être régénéré avec tous les emails collectés.

## Fichiers importants

- `attente/emails_utils.py` : logique de chiffrement, validation, PDF
- `attente/views.py` : route de collecte et route de téléchargement PDF
- `attente/urls.py` : routes de l'application
- `attente/templates/index.html` : interface utilisateur
- `config/settings.py` : configuration Django
- `data_emails/` : stockage sécurisé des données
>>>>>>> main

## Personnalisation

- Modifier `DATE_CIBLE` dans `attente/emails_utils.py` pour définir la date de fin du compte à rebours.
- Personnaliser le contenu et le style dans `attente/templates/index.html`.
- Ajuster le CSS Tailwind dans `static/`.

<<<<<<< HEAD
- La date du compte à rebours dans `attente/emails_utils.py` (variable `DATE_CIBLE`) — doit correspondre à la date affichée côté template
- L'adresse email destinataire du rapport final (`EMAIL_DESTINATAIRE` dans `emails_utils.py`)
- Le contenu du texte dans le template
- Les styles Tailwind dans les fichiers statiques

## Sécurité — points d'attention

- Le dossier `data_emails/` (clé de chiffrement, emails, hashes, PDF) contient des données personnelles et **ne doit jamais être versionné dans Git**. Il est déjà listé dans `.gitignore`.
- Le fichier `.env` contient le mot de passe d'application Gmail — **ne doit jamais être versionné**. Il est déjà listé dans `.gitignore`.
- En production, préférez stocker la clé de chiffrement et les secrets email dans un gestionnaire de secrets plutôt que dans des fichiers locaux.

## Notes techniques

- Le projet ne dépend d'aucune base de données : les sessions Django utilisent le backend `signed_cookies` plutôt que la base par défaut, ce qui permet de se passer complètement de `db.sqlite3`, des migrations et d'un compte superuser.
- Sous Windows, un bug de certificats SSL (`CERTIFICATE_VERIFY_FAILED`) peut survenir lors de l'envoi SMTP sur certaines versions de Python. Le projet contourne ce problème via `truststore` (utilisation du magasin de certificats natif de Windows).
=======
## Sécurité

- Ne jamais versionner `data_emails/`.
- `data_emails/cle_secrete.key` est nécessaire pour déchiffrer les emails.
- Le PDF contient des données personnelles, gardez le dossier privé.

## Notes

Ce projet est conçu pour être une page d'attente simple et sécurisée, avec une collecte d'emails chiffrée et un rapport PDF final destiné au staff administratif.
>>>>>>> main
