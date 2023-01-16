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

## Mise en place d'un serveur

- ouverture des port et firewall
- fail2ban (/etc/fail2ban/jail.conf)
- modifier le mot de passe root
- ajouter un utilisateur pour le phpmyadmin
- ajouter un utilisateur pour se connecter a distance
> CREATE USER 'sae_kivy'@'%' IDENTIFIED BY 'Sae302!client';
> GRANT SELECT, INSERT, UPDATE, DELETE ON universite.* TO 'sae_kivy'@'%';
> FLUSH PRIVILEGES;  
- exporter importer notre base de donneés
- crontab pour notre recupearation d'image
- systemd pour le serveur http python

