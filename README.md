# Page d'attente

Ce projet est une page de lancement moderne construite avec Django pour présenter un site ou un événement avant sa mise en ligne. Elle affiche un compteur de temps restant et un formulaire d'inscription par e-mail, avec une collecte d'emails chiffrée et un export PDF automatique une fois le compte à rebours terminé.

## Fonctionnalités

- Page d'accueil responsive et élégante
- Compte à rebours dynamique
- Formulaire d'inscription par email
- Collecte d'emails **chiffrée** (chiffrement réversible, aucun email stocké en clair sur le disque)
- Détection automatique des doublons (via hash SHA-256, sans jamais déchiffrer)
- Téléchargement du PDF réservé aux comptes admin (`pour télécharger d'abord faire python manage.py migrate ensuite on vas crée un superuser et partir sur cet url 'http://127.0.0.1:8000/telecharger-pdf/'`)
- Génération automatique d'un **rapport PDF** une fois le compte à rebours terminé et le téléchargement éfectuer
- Interface stylée avec Tailwind CSS
- Base Django prête à exécuter

## Technologies utilisées

- Python
- Django
- SQLite
- Tailwind CSS
- HTML/CSS/JavaScript
- `cryptography` (chiffrement des emails)
- `reportlab` (génération du PDF)

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
pip install django cryptography reportlab
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

2. Créer un superuser (nécessaire pour accéder au téléchargement du PDF) :

```bash
python manage.py createsuperuser
```

3. Démarrer le serveur Django :

```bash
python manage.py runserver
```

4. Ouvrir l'application dans votre navigateur :

```text
http://127.0.0.1:8000/
```

## Structure du projet

```text
page_attente/
├── attente/              # Application Django (vues, urls, logique email)
├── config/               # Configuration du projet
├── static/               # Fichiers statiques CSS/JS
├── templates/            # Templates principaux
├── data_emails/          # Données de collecte (généré automatiquement, NE PAS versionner)
│   ├── cle_secrete.key       # Clé de chiffrement — à protéger absolument
│   ├── emails_chiffres.txt   # Emails chiffrés, un par ligne
│   ├── emails_hashes.txt     # Empreintes SHA-256 (déduplication)
│   └── emails_finaux.pdf     # Rapport final (généré après le compte à rebours et le téléchargement)
├── manage.py             # Point d'entrée Django
├── package.json          # Dépendances frontend
└── db.sqlite3            # Base de données locale
```

## Fonctionnement de la collecte d'emails

1. Chaque email soumis via le formulaire est validé (format), puis vérifié pour éviter les doublons (comparaison de hash SHA-256, sans jamais déchiffrer les emails existants).
2. L'email est ensuite chiffré (chiffrement symétrique réversible) avant d'être écrit dans `emails_chiffres.txt`. Le fichier texte ne contient donc jamais d'email lisible.
3. La clé de chiffrement (`cle_secrete.key`) est générée automatiquement au premier email collecté, et réutilisée ensuite. **Sans cette clé, les emails sont définitivement illisibles.**
4. Une fois la date cible du compte à rebours atteinte, le PDF final (`emails_finaux.pdf`) est généré à partir des emails déchiffrés.
5. Un administrateur connecté peut télécharger ce PDF à jour via la route `'http://127.0.0.1:8000/telecharger-pdf/'` (protégée, inaccessible aux visiteurs non-admin).

## Personnalisation

Vous pouvez modifier :

- La date du compte à rebours dans `attente/emails_utils.py` (variable `DATE_CIBLE`) — doit correspondre à la date affichée côté template
- Le contenu du texte dans le template
- Les styles Tailwind dans les fichiers statiques

## Sécurité — points d'attention

- Le dossier `data_emails/` (clé de chiffrement, emails, hashes, PDF) contient des données personnelles et **ne doit jamais être versionné dans Git**. :
  ```text
  data_emails/
  ```
- La route `'http://127.0.0.1:8000/telecharger-pdf/'` est protégée par `@staff_member_required` : seul un compte admin Django connecté peut y accéder.


## Notes

Ce projet est actuellement configuré comme une page d'attente pour la PyCon Côte d'Ivoire 2027, avec collecte sécurisée des emails des personnes intéressées avant l'ouverture officielle du site complet.