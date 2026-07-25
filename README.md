# Page d'attente

Ce projet est une page de lancement moderne construite avec Django pour présenter un site ou un événement avant sa mise en ligne. Elle affiche un compteur de temps restant et un formulaire d'inscription par e-mail.

## Fonctionnalités

- Page d'accueil responsive et élégante
- Compte à rebours dynamique
- Formulaire d'inscription par email
- Interface stylée avec Tailwind CSS
- Base Django prête à exécuter

## Technologies utilisées

- Python
- Django
- SQLite
- Tailwind CSS
- HTML/CSS/JavaScript

## Prérequis

Assurez-vous d'avoir installé :

- Python 3.10 ou plus
- pip
- Node.js et npm

## Installation

1. Cloner le projet :

```bash
git clone <url-du-projet>
cd page_attente
```

2. Créer un environnement virtuel :

```bash
python -m venv .venv
```

3. Activer l'environnement virtuel :

Sur Windows :

```bash
.venv\Scripts\activate
```

Sur Linux/macOS :

```bash
source .venv/bin/activate
```

4. Installer les dépendances Python :

```bash
pip install django
```

5. Installer les dépendances JavaScript :

```bash
npm install
```

## Lancer le projet

1. Appliquer les migrations :

```bash
python manage.py migrate
```

2. Démarrer le serveur Django :

```bash
python manage.py runserver
```

3. Ouvrir l'application dans votre navigateur :

```text
http://127.0.0.1:8000/
```

## Structure du projet

```text
page_attente/
├── attente/              # Application Django
├── config/               # Configuration du projet
├── static/               # Fichiers statiques CSS/JS
├── templates/            # Templates principaux
├── manage.py             # Point d'entrée Django
├── package.json          # Dépendances frontend
└── db.sqlite3            # Base de données locale
```

## Personnalisation

Vous pouvez modifier :

- La date du compte à rebours dans la vue Django
- Le contenu du texte dans le template
- Les styles Tailwind dans les fichiers statiques

## Notes

Ce projet est actuellement configuré comme une page d'attente pour un événement ou un lancement à venir.
