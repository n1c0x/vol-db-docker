# vol-db-docker

## Installation

### Prérequis

Docker v1.13+

### Compilation du conteneur

`sudo docker-compose build`. 

En cas d'utilisation d'un proxy, il faut utiliser la commande suivante au lieu de la commande ci-dessus : 
`sudo docker-compose build --build-arg HTTP_PROXY=http://xx.xx.xx.xx:xx --build-arg HTTPS_PROXY=http://xx.xx.xx.xx:xx`

Si l'erreur suivante apparait, il faut lancer le service docker avant la compilation : `sudo systemctl start docker` 
`ERROR: Couldn't connect to Docker daemon at http+docker://localhost - is it running?` 

### Lancement du conteneur
`sudo docker-compose up`

## Fait

- Formulaires
    - Ajout/modification/suppression de codes AITA
    - Ajout/modification/suppression d'avions (immatriculation + type + mono- ou multimoteur)
    - Ajout/modification/suppression de personnes
    - Ajout/modification/suppression d'un vol
- Liste de tous les vols 
    - Colonnes affichées
        - Date
        - Aéroports de départ et d'arrivée
        - Durée de vol de jour/nuit
        - Commandant de bord/copilote
        - Fonctione
        - Poste
    - Filtres possibles
        - Date (toutes les dates, Aujourd'hui, les 7 derniers jours, ce mois-ci et cette année)
        - Arrivée IFR (Oui ou Non)
    - Barre de recherche sur les noms et prénoms des protagonistes (CDB, OPL, OBS1, OBS2 et Instructeur)

## A faire

- Ajouter d'autres filtres


## Source

- https://docs.docker.com/compose/django/ 
- https://www.supinfo.com/articles/single/5779-bien-debuter-avec-django-docker
