# **[SynTriplets](https://github.com/Hefr-y/SynTriplets)**

![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Hefr-y/pinyinALAO/blob/main/LICENSE)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

Le projet consiste à écrire un programme en python 3 qui utilise l’analyse syntaxique et les plongements lexicaux pour extraire les mentions de type **_nourriture_**, **_boisson_** et **_service_**, à partir d’avis sur des restaurants écrits par des clients. Dans le cadre d'un projet de cours [Syntaxe / sémantique](https://formations.univ-grenoble-alpes.fr/fr/catalogue-2021/master-XB/master-sciences-du-langage-IBC7OSQ4/parcours-industrie-de-la-langue-IBC7YS7U/ue-modeles-de-conception-ecrit-parole-KMZ3275F/syntaxe-semantique-KMZ350I6.html).

On utilise spaCy pour l’analyse syntaxique et la librairie gensim de Python pour l’accès au plongements lexicaux.

Basé sur [spaCy==2.3.5](https://spacy.io/), [fr_core_news_md](https://spacy.io/models/fr#fr_core_news_md) de spaCy et [gensim==4.1.2](https://github.com/RaRe-Technologies/gensim).

- GitHub : https://github.com/Hefr-y/SynTriplets
- Python version : 3.8

## Table des matières

- [Installation](#installation)
- [Usage](#usage)
- [API](#api)
- [Exemple](#exemple)

## Installation

Cloner le projet depuis notre site Github : 
```bash
$ git clone https://github.com/Hefr-y/projet_syn.git
```

Ce projet utilise [spaCy](https://spacy.io/) et [gensim](https://github.com/RaRe-Technologies/gensim). Allez les voir si vous ne les avez pas installés localement :

```bash
$ pip install -U gensim==4.1.2
```

```bash
$ pip install -U spacy==2.3.5
```

### Méthode d'installation recommandée

>
>Afin de ne pas polluer l'environnement de votre répertoire de travail actuel, nous vous recommandons d'installer toutes les dépendances de ce projet via [pipenv](https://github.com/pypa/pipenv).

Cloner le projet depuis notre site Github : 

```bash
$ git clone https://github.com/Hefr-y/projet_syn.git
```

**[Pipenv](https://github.com/pypa/pipenv) peut être installé avec Python 3.6 et plus.**

Si vous utilisez Debian Buster+ 

```bash
$ sudo apt install pipenv
```

Ou, si vous utilisez Windows :

```bash
$ pip install --user pipenv
```

Sinon, consultez la [documentation de pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today) pour obtenir des instructions.


Ensuite, sous le répertoire générale du projet où se trouvent les fichiers ***Pipfile*** et ***Pipfile.lock***

```bash
$ pipenv install
```

✨🍰✨


## Usage
Pour lancer la procédure, suivez les étapes suivantes:

1. Sous **le répertoire générale** du projet, démarrer l'environnement virtuel

> Si vous n'avez pas installé pipenv, vous pouvez ignorer cette étape.

```bash
$ pipenv shell
```

2. Aller dans le répertoire du projet via la commande ***cd*** (Ex:si le projet est dans ***Desktop***)
```bash
$ cd Desktop
```

3. Accéder au projet via le ***cd Nom_du_Projet*** où se trouvent le fichier ***run.py*** (Ex:si le projet est ***SynTriplets***)
```bash
$ cd SynTriplets
```

4. Démarrage
```bash
$ python run.py votre_fichier_textes
```


## Exemple

Le [testDemo.txt](https://github.com/Hefr-y/projet_syn/blob/main/SynTriplets/testDemo.txt) dans le dossier du projet est utilisé dans ce cas.

Veuillez consulter l'image ci-dessous:

![image](https://github.com/Hefr-y/projet_syn/blob/main/screenshot.png)


Enfin, un fichier **_resultats.json_** est généré dans le répertoire de travail où sont stockés les résultats de l'analyse.


## API

> Pour API plus détaillées, veuillez consulter le fichier [run.py](https://github.com/Hefr-y/projet_syn/blob/main/SynTriplets/run.py).
>
