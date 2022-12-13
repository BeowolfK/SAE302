# SAE302
SAE 302 - Developpement d'applications communicante

## Représentation de la base de données

![Représentation](./image//mcd.jpg)

## Utilisation de Docker

[Télécharger Docker](https://docs.docker.com/desktop/) selon le système d'exploitation
Pour lancer les containers, la commande est la suivante :

```bash
docker-compose up
```

Nous pouvons acceder a PHPMyAdmin sur l'URL `http://localhost:8080`.
Pour acceder a la base de donnée, nous pouvons nous connecter sur `localhost:3307`
Nous pouvons aussi acceder a la base de données directement sur le container grace a la commande

```bash
docker exec -it <CONTAINER-ID> bash
```

Ici, `CONTAINER-ID = sae302-db-1`.

Grace aux volumes persistants, nos bases de données sont dans le dossier `./database`

## Serveur Web 

Pour installer les paquets nécessaire, nous pouvons faire la commande suivante:

```bash
python -m pip install -r requirements.txt
```

La page web est ensuite visible, une fois le programme lancé, sur l'ip de la machine (Port 80 par défaut).

Sur serveur Linux, pour lancer le site web en production, il faut utiliser la commande :

```bash
gunicorn -w -4 --reload -b localhost:80 "web.flask-app:home()"
```
