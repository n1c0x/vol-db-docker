# vol-db-docker

## Installation

### Prérequis

#### Logiciels

- python3.7
- python3.7-dev
- default-libmysqlclient-dev 
- mariadb-server

### Installation des prérequis python

```pip3 install django>=2 psycopg2-binary admin-totals mysqlclient```
```pip3 install -r requirements.txt```

#### Configuration de la base de données

##### Création de la base de données
```MariaDB [(none)]> create database voldb character set 'utf8';```

##### Création de l'utilisateur et assignation des droits
```MariaDB [(none)]> CREATE USER voldb@localhost IDENTIFIED BY 'password';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON voldb.* TO 'voldb'@'localhost';```

##### Création du fichier de configuration mysql
Il faut créer le fichier ```/etc/mysql/conf.d/mysql.cnf``` sur Debian
Il faut créer le fichier ```/etc/my.cnf.d/client.cnf``` sur CentOS/RedHat

Contenu du fichier :
```
[client]
database = voldb
host = localhost
user = voldb
password = password
default-character-set = utf8
```

##### Migration de la base de données
```python3.7 manage.py makemigrations vol```
```python3.7 manage.py migrate```

### Lancement du service
```python manager.py runserver 0.0.0.0:8000```

### Création de l'administrateur django
```$> python3 manage.py createsuperuser```

### Création du profile de l'administrateur (temporaire, à changer)
```MariaDB [(none)]> insert into vol_profile (user_id, client_type, current_position, employer) values ("1","Gratuit","AUTRE","Air France");```


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
- Ajout/modification/suppression de codes IATA
    - Ajout/modification/suppression d'avions (immatriculation + type + mono- ou multimoteur)
    - Ajout/modification/suppression de personnes

## A faire

- Voir Issues
- Filtres possibles
        - Date (toutes les dates, Aujourd'hui, les 7 derniers jours, ce mois-ci et cette année)
        - Arrivée IFR (Oui ou Non)
    - Barre de recherche sur les noms et prénoms des protagonistes (CDB, OPL, OBS1, OBS2 et Instructeur)


## Source
- https://docs.djangoproject.com/fr/2.1
- https://tutorial.djangogirls.org/fr/

### Déploiement
- https://docs.djangoproject.com/en/2.1/howto/deployment/
