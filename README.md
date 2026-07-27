# Page d'attente PyCon CI 2027

Projet Django minimal pour une page d'attente avec compteur, collecte d'emails chiffrée et génération de rapport PDF.

## Présentation

Cette application propose :

- une page d'accueil responsive
- un compteur de compte à rebours dynamique
- un formulaire d'inscription par email
- une collecte d'emails chiffrée et immuable
- une déduplication par hash SHA-256
- un téléchargement PDF protégé pour les administrateurs

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

## Prérequis

- Python 3.10+ ou version compatible
- pip
- Node.js et npm

## Installation

```bash
git clone <url-du-projet>
cd page_attente
python -m venv .venv
.venv\Scripts\activate
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
```

## Comment fonctionne la collecte d'emails

1. L'utilisateur soumet un email via le formulaire.
2. Le backend valide le format et normalise l'email.
3. Le hash SHA-256 est généré et comparé aux hashes existants.
4. Si l'email est nouveau, il est chiffré et sauvegardé.
5. Les hash sont stockés pour empêcher les doublons.
6. Lorsque la date cible est dépassée, le PDF peut être régénéré avec tous les emails collectés.

## Fichiers importants

- `attente/emails_utils.py` : logique de chiffrement, validation, PDF
- `attente/views.py` : route de collecte et route de téléchargement PDF
- `attente/urls.py` : routes de l'application
- `attente/templates/index.html` : interface utilisateur
- `config/settings.py` : configuration Django
- `data_emails/` : stockage sécurisé des données

## Personnalisation

- Modifier `DATE_CIBLE` dans `attente/emails_utils.py` pour définir la date de fin du compte à rebours.
- Personnaliser le contenu et le style dans `attente/templates/index.html`.
- Ajuster le CSS Tailwind dans `static/`.

## Sécurité

- Ne jamais versionner `data_emails/`.
- `data_emails/cle_secrete.key` est nécessaire pour déchiffrer les emails.
- Le PDF contient des données personnelles, gardez le dossier privé.

## Notes

Ce projet est conçu pour être une page d'attente simple et sécurisée, avec une collecte d'emails chiffrée et un rapport PDF final destiné au staff administratif.