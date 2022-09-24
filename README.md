Zython
======

[http://zython.me](http://zython.me)




Qu'est-ce ?
-----------

Zython est une application en ligne d'aide à la conception de recettes de bière et est logée sur https://zython.me


Pourquoi ?
----------

Parce que le milieu brassicol manque d'un logiciel qui permette toutes ces choses à la fois : 

 * d'en disposer gratuitement
 * de choisir les unités locales (métrique/impérial...)
 * de pouvoir s'en servir quelque soit l'ordinateur utilisé
 * partager une recette privée avec quelqu'un pour la travailler
 * échanger des commentaires sur une recette
 * vérifier la justesse de la recette avec un style BJCP2008


Equivalents
-----------

(ceux que je connais / pas forcément gratuits / pas forcément en français)

 * http://joliebulle.tuxfamily.org/
 * http://hopville.com/
 * http://beerrecipes.org/
 * http://beersmith.com/
 * http://www.tastybrew.com/


Participer
----------

Vous pouvez participer à ce projet open source et gratuit lancé en 2012 via Tipee : https://tipeee.com/zythonme


Contribuer
----------

Le déploiement de l'application en local nécessite d'avoir installé au
préalable [Docker-Compose](https://docs.docker.com/compose/install/).

Créer un fichier `.env` à partir du fichier `.env.template` et renseigner les
diverses variables d'environnement.

Lancer le conteneur :

```bash
$ docker-compose up web
```

Le serveur devrait être accessible depuis un navigateur à l'URL
`http://127.0.0.1:[ZYTHON_PORT]` (avec comme valeur pour `ZYTHON_PORT` celle
indiquer dans le fichier `.env`).


TODO list
=========

N'hésitez pas à me faire part de vos remarques via le Tipee ci-dessus. Ce sont vos retours qui me permettent de peser les priorités

 * Ecrire plus de tests automatiques
 * Ajout d'eau dans la recette à n'importe quel moment
 * Ajout de grain pendant l'ébullition
 * Ajout d'épice pendant l'empattage
 * Différencier visuellement l'empattage de l'ébullition (fiche recette plus élaborée ?)
 * Export au format BeerXML


Licence
=======

    /*
     * ----------------------------------------------------------------------------
     * "THE BEER-WARE LICENSE" (Revision 42):
     * <phk@FreeBSD.ORG> wrote this file. As long as you retain this notice you
     * can do whatever you want with this stuff. If we meet some day, and you think
     * this stuff is worth it, you can buy me a beer in return Poul-Henning Kamp
     * ----------------------------------------------------------------------------
     */

