# vol-db-docker

## Installation

### Prerequisites

#### Software

- python3.7
- python3.7-dev
- default-libmysqlclient-dev
- mariadb-server

### Installation of python prerequisites

```bash
$> pip3 install -r requirements.txt
```

#### Databse configuration

##### Database creation

```sql
MariaDB [(none)]> create database voldb character set 'utf8';
```

##### Database user creation and rights assignments

```sql
MariaDB [(none)]> CREATE USER voldb@localhost IDENTIFIED BY 'password';
MariaDB [(none)]> GRANT ALL PRIVILEGES ON voldb.* TO 'voldb'@'localhost';
```

##### MySQL configuration file

###### Debian

You need to create the file here : `/etc/mysql/conf.d/mysql.cnf`

###### CentOS/RedHat

You need to create the file here `/etc/my.cnf.d/client.cnf`

###### File content

```apache
[client]
database = voldb
host = localhost
user = voldb
password = password
default-character-set = utf8
```

##### Environment variable
To use the specific settings file, we need to define which will be used as an environment variable. Or add `--settings=voldb.settings.<environment>` at the end of each command. 

###### Development
```bash
export DJANGO_SETTINGS_MODULE=voldb.settings.development
```

###### Staging
```bash
export DJANGO_SETTINGS_MODULE=voldb.settings.staging
```

###### Production
```bash
export DJANGO_SETTINGS_MODULE=voldb.settings.production
```

##### Database migration

```bash
$> python3.7 manage.py makemigrations vol
$> python3.7 manage.py migrate
```

### Starting in development mode

```bash
$> python manager.py runserver 0.0.0.0:8000 
```

### Django superuser creation

```bash
$> python3 manage.py createsuperuser
```


## Done

- Forms
  - Adding/deleting a flight
- List of all flights
- User management (views and templates)
  - Login
  - Logout
  - Change of password
  - Password Reset
- Homepage
- Adding/modifying/deleting assets

## ToDo

- See Issues

## Source

- [https://docs.djangoproject.com/fr/2.1](https://docs.djangoproject.com/fr/2.1)
- [https://tutorial.djangogirls.org/fr/](https://tutorial.djangogirls.org/fr/)

### Deployment

- [https://docs.djangoproject.com/en/2.1/howto/deployment/](https://docs.djangoproject.com/en/2.1/howto/deployment/)
