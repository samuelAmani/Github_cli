# GitHub CLI Explorer

[![CI Test Suite](https://github.com/samuelAmani/Github_cli/actions/workflows/ci.yml/badge.svg)](https://github.com/samuelAmani/Github_cli/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un outil en ligne de commande (CLI) moderne, ergonomique conçu en Python pour inspecter les comptes utilisateurs, dépôts et activités publiques sur GitHub en temps réel.

Ce projet met en pratique une architecture logicielle découplée (Separation of Concerns), une gestion des erreurs réseau (et de quota), une suite de tests unitaires avec isolation par mocks, ainsi qu'un pipeline d'intégration continue (CI) automatisé.

---

## Fonctionnalités Principales

* **Profil utilisateur enrichi (`profile`) :** Affiche l'identité complète, la biographie, la localisation et le volume de dépôts publics dans un panneau visuel stylisé.
* **Exploration des dépôts (`repos`) :** Liste des dépôts publics, avec mise en avant du langage prédominant et du compteur d'étoiles.
* **Dépôts favoris (`starred`) :** Accès direct aux projets surveillés ou marqués par un utilisateur.
* **Journal d'activité (`activity`) :** Historique des derniers événements publics (`PushEvent`, `WatchEvent`, `CreateEvent`).
* **Mode Diagnostic (`--verbose`) :** Traçabilité des requêtes HTTP et des en-têtes sans encombrer la vue standard.
* **Robustesse réseau :** Interception des erreurs 404 (utilisateur inexistant), 401 (problème d'authentification) et 403/429 (dépassement de quota avec indication du moment de réinitialisation).

---

## Aperçu des Commandes

| Commande | Description | Exemple |
| :---     | :---        | :---    |
| `profile`| Affiche la fiche synthétique d'un profil | `python -m github_cli.cli profile octocat` |
| `repos`  | Liste les dépôts publics (paramètre `--limit`) | `python -m github_cli.cli repos torvalds --limit 5` |
| `starred` | Liste les projets mis en favoris | `python -m github_cli.cli starred octocat` |
| `activity`| Liste les actions récentes de l'utilisateur | `python -m github_cli.cli activity torvalds` |

---

## Prérequis & Stack Technique

* **Langage :** Python 3.11+
* **Framework CLI :** [Typer](https://typer.tiangolo.com/) (basé sur Click)
* **Moteur de rendu terminal :** [Rich](https://rich.readthedocs.io/)
* **Transport HTTP :** [Requests](https://requests.readthedocs.io/)
* **Tests & Mocks :** [Pytest](https://docs.pytest.org/) & [Responses](https://github.com/getsentry/responses)
* **CI/CD :** GitHub Actions

---

## Guide d'Installation

### 1. Cloner le projet
```bash
git clone https://github.com/samuelAmani/Github_cli.git
cd Github_cli
2. Mettre en place l'environnement virtuel
Bash
# Création de l'environnement virtuel
python -m venv .venv

# Activation :
# Sur Linux / macOS :
source .venv/bin/activate
# Sur Windows (cmd / PowerShell) :
.venv\Scripts\activate
3. Installer les dépendances requises
Bash
pip install --upgrade pip
pip install -r requirements.txt
    
    Configuration du Jeton GitHub (Optionnel)
Par défaut, l'API publique de GitHub restreint les requêtes non-authentifiées à 60 requêtes par heure. L'ajout d'un jeton d'accès personnel (PAT) augmente ce plafond à 5 000 requêtes par heure.

Générez un jeton classique ou fine-grained sur GitHub (Settings > Developer settings > Personal access tokens). Aucun scope spécifique n'est requis pour lire les données publiques.

Création un fichier .env à la racine de votre projet :

Bash
touch .env
Renseignez votre jeton dans le fichier :

Code snippet
GITHUB_TOKEN=votre_jeton_personnel_ici
(Le fichier .env est automatiquement ignoré par .gitignore pour prévenir toute fuite de secret).

Exemples d'Utilisation
Consulter un profil utilisateur
Bash
python -m github_cli.cli profile octocat
Filtrer les dépôts avec une limite
Bash
python -m github_cli.cli repos octocat --limit 3
 
Bash
python -m github_cli.cli profile octocat --verbose
Afficher le manuel d'aide interactif
Bash
python -m github_cli.cli --help
python -m github_cli.cli repos --help
   
    Exécution des Tests Automatisés
Le projet comprend une suite complète de tests unitaires qui simule les réponses HTTP sans consommer de quota GitHub.

Bash
pytest -v

 Structure du Répertoire
Plaintext
Github_cli/
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline d'Intégration Continue (GitHub Actions)
├── github_cli/
│   ├── __init__.py
│   ├── api_client.py          # Logique HTTP, session et construction des requêtes
│   ├── cli.py                 
│   ├── exceptions.py          # Gestion des erreurs de domaine 
│   └── logger.py              
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py     
│   └── test_cli.py            
├── .env.example               # Modèle de configuration pour le token d'API
├── .gitignore                 
├── requirements.txt           
└── README.md                  # Documentation principale
   Licence
Ce projet est distribué sous la licence MIT.


