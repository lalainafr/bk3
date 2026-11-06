# bk3

# bk3

# "La Grance Cinema"

[![CircleCI](https://lrajaonahsoa.pythonanywhere.com/)](https://github.com/lalainafr/bk3.git)

## Description :

Réaliser une application qui permet de gerer la réservation en ligne d'une sale de cinéma. L'application offre les fonctionalités qui permettent la création de compte client et admin, la gestion des salles, des films, des événéments, des séances avec des horaires d'ouverture. La gestion des réservations, le paiement jusqu'à la mise à disposition d'un ticket

# Détails du projet

### Objectifs :

Le projet consiste à développer une application web de réservation de places de cinéma en ligne afin de moderniser le fonctionnement du cinéma et d’améliorer l’expérience des spectateurs.

L’objectif principal est d’augmenter la fréquentation du cinéma de 30 % en 12 mois, notamment pendant le Jazz Festival, en permettant aux clients de consulter les séances, de visualiser les places disponibles en temps réel, de réserver leurs billets à distance et d’obtenir un billet dématérialisé.

L’application permettra également à l’administration de gérer la programmation, de suivre les réservations, d’analyser le taux de remplissage des salles et d’anticiper les périodes de forte affluence.

### Résultats attendus :

Réduire les files d’attente et les temps d’attente au guichet.

Améliorer l’expérience et la satisfaction des clients.

Optimiser le remplissage des salles.

Attirer une clientèle touristique habituée aux services numériques.

Augmenter le chiffre d’affaires du cinéma.

#### Profils utilisateurs :

##### Visiteur :

- Le VISITEUR poura consulter la page d'accueil, les films et les evenements avec les horaires des séances proposées.

##### Client :

- Le CLIENT peut soumettre une demande de création de compte pour les nouveaux clients. La création de compte s’effectue à travers un formulaire. une fois connecté, le client sera en mesure de choix des séances et les mettre dans le panier. Il pourra consulter son panier, changer le nombre de place, rajouter d'autres séances et supprimer des séances dans le panier

##### Staff :

- Le STAFF aura accès à une interface dashboard pour consulter les résevations des clients, programmer les salles, les films, les événements, et les séances (creér, consuler, modifier, et supprimer). Il pourra accèder aussi avoir le taux de remplissage des salles, des créneaux horaires ainsi que des films ou événements.

##### Admin :

- L'ADMIN aura accès à une interface admin pour gérer tout le projet.

### Descriptions des fonctionnalités :

#### Souscription et connexion :

Tout VISITEUR aura la possibilité d'acceder à une page pour s'inscrire, ensuite une autre page lui permettra de se connecter en entrant ses identifinats (email et mot passe). Les mots de passe seront sécurisés.

#### Dashboard :

Le STAFF aura la possibilté de gérer (consulter, ajouter, modifier, supprimer) les salles, les films, les événements, et les séances
Les séances programmées sont visibles sur la page d'accueil du site web sur le menu 'film' ou 'événement' sur le header.

#### Reservation :

Chaque utilisateur (visiteur, client) pourra voir et choisir les séances film ou événement qui sont programmées.
Afin de mettre une séance dans le panier, le visiteur doit se connecter avec sont login et mot de passe, dans le cas contraire il doit créer un compte.
Il pourra ensuite rajouter la quantité, rajouter d'autres séances et supprimer des séances dans le panier

Le panier contient les détails des séances commandées, leurs quantités, prix. Le sous-total ainsi que le Total sont calculé automatiquement

#### Paiement :

Le client aura la possibilité de payer les séances commandées dans le panier. La validation se fait à partir des informations qu'il doit rentre ( date d'anniversaire, carte bancaire, nom de la banque).
Ces informations doivent étre correctes et seront vérifiées (pour l'examen) à partir d'un end point (https://lrajaonahsoa.pythonanywhere.com/list-profile) contenant le profil de chaque client ( date d'anniversaire, carte bancaire, nom de la banque). Le profil du client est créé automatiquement de manière aléatoire à la création du compte.
Pas de rechargement de page lors de la vérification des informations du client

#### Ticket :

Une fois le paiement validé, un ticket avec un qr-code sera fourni au client.
Le client pourra voir le détail de son ticket à partir du qr-code sinon à partir du bouton détail sur le ticket
Le client aura la liste des tickets qu'il a achétés dans son compte personnel

Quelques contraintes ont été mises en place:

- Lors de la programmation des séances, le staff pourra choisir soit un film soit un événement. Le DOM a été manipulé afin de faire en sorte que l'autre soit désactivé lors de la sélection d'un film ou événement
- Lors de la programmation des séances, un message d'erreur est generé pour informer si la salle avec le créneau séléctionné a déjà été pris

Les places disponibles pour les dates selectionnées sont mises à jours (decrementé) quand un client réserve une séance

# Guide d'utilisation

Le manuel d'utilisation se trouve dans le dossier pdf.

# Déploiement

Afin de déployer le projet sur pythonanywhere. Il est important d'avoir créer un compte sur celui-ci, louer un hebergement

Configuration:

Sur PythonAnywhere

Creér un compte sur pythonanywhere
Lrajaonahsoa
Customer\*123456

Bash

- clonner le projet en github
- créer un environement virtuel
  mkvirtualenv --python=/usr/bin/python3.9 myenv

Web

- new web app / next/ manual / python version
- code/ source code
  working directory + nom projet dans github (renomer mysite)
  /home/lrajaonahsoa/bloc3_project

Configurer WSGI configuration file

Configurer le bloc de l’environnement virtuel

Bash

- Installer django
  pip install django

- On entre dans le projet. cd nom du projet
  pip install -r requirements.txt (installer les dépendances)
  python3.9 manage.py collectstatic (installer static files)
- Files/ … entrer dans settings du projet (venant de git)

Pip3 instal pymysql

Project/**init** .py
import pymysql
pymysql.install_as_MySQLdb()

Impelmenting Mysql database in python anywhere
Database /New pwd/ iniatrialize MySQL
configurer base de données dans file/project/settings.py

Bash
Python manage.py migrate
Pip instal mysqlclient

- Parametrer la base données( nom d'utilisateur et mot de passe)
- Parametrer la version Python

# Installation en local

Pour installer le projet en local. Vous devez avoir un environement de développement correctement configuré.

Une fois cela fait :

- Cloner le projet
    - `git clone https://github.com/lalainafr/bk3.git`
- Créer un fichier .env.local

pip3 freeze > requirements.txt

Install Django

Create project
django-admin startproject myproject

Create app
python manage.py startapp myapp

lancer le projet

python manage.py runserver

configurer setting: nom app, base de données, staticfiles...

initialiser le fihcier GIT
