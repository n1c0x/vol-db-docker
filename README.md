# vol-db-docker

## Installation

### Prérequis

Python 3.6
Python 3.6 devel

### Installation des prérequis python

psycopg2-binary
admin-totals
mysqlclient

### Lancement du service
python manager.py runserver

## Fait

- Formulaires
    - Ajout/modification/suppression d'un vol
- Liste de tous les vols 
    - Colonnes affichées
        - Date
        - Aéroports de départ et d'arrivée
        - Durée de vol de jour/nuit
        - Commandant de bord/copilote
        - Fonctione
        - Poste
- Gestion d'utilisateur (vues et gabarits)
    - Login
    - Logout
    - Changement de mot de passe
    - Réinitialisation de mot de passe
- Page d'accueil

## A faire

- Voir Issues
- Ajout/modification/suppression de codes IATA
    - Ajout/modification/suppression d'avions (immatriculation + type + mono- ou multimoteur)
    - Ajout/modification/suppression de personnes
- Filtres possibles
        - Date (toutes les dates, Aujourd'hui, les 7 derniers jours, ce mois-ci et cette année)
        - Arrivée IFR (Oui ou Non)
    - Barre de recherche sur les noms et prénoms des protagonistes (CDB, OPL, OBS1, OBS2 et Instructeur)


## Source
- https://docs.djangoproject.com/fr/2.1
- https://tutorial.djangogirls.org/fr/

### Déploiement
- https://docs.djangoproject.com/en/2.1/howto/deployment/
