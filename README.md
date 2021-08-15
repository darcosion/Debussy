# Debussy - Collect on Soundcloud

## Description & fonctionnalités

Debussy est un outil d'OSINT permettant notamment de récupérer les commentaires donné aux musiques d'un profile sur soundcloud

```bash
$ python3 main.py -h
Debussy par darcosion (https://github.com/darcosion)
usage: main.py [-h] [-u URL] [-t TOKEN] [-b] [-l] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     user à investiguer
  -t TOKEN, --token TOKEN
                        client_id token
  -b, --biggest-com     people who comment the most
  -l, --list-com        list of com
  -c, --cloudword       cloud of words

```

Il possède trois options pour cela :
 - biggest-com qui liste les profiles des gens par ordre de fréquence, la personne ayant commenté la première se retrouvant donc en premier
 - list-com qui liste l'intégralité des commentaires
 - cloudword qui liste les mots employés dans les commentaires par ordre d'importance

 ## installation

 `pip3 install -r requirements.txt`

note : `spacy` est une dépendance permettant de faire la partie "nuage de mots" (cloudword). Si vous n'utilisez pas cette fonctionnalité, pas besoin d'utiliser spacy.
