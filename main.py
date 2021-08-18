#!/usr/bin/env python3

#import globaux
import argparse, csv, json


# imports custom rich
from rich.console import Console as richConsole
from rich.progress import track as richTrack
from rich.panel import Panel as richPanel
from rich.table import Table as richTable

#import locaux
import soundcloud

#on vérifie qu'on est bien lancé en "main" :
if __name__ == "__main__":
    #on lance rich
    console = richConsole()

    console.print("Debussy par darcosion (https://github.com/darcosion)")

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str,
                        help="user à investiguer")
    parser.add_argument("-b", "--biggest-com", action='store_true',
                        help="personnes qui commentent le plus")
    parser.add_argument("-l", "--list-com", action='store_true',
                        help="list de com")
    parser.add_argument("-c", "--cloudword", action='store_true',
                        help="occurence de mots")
    parser.add_argument("-e", "--export", type=str,
                        help="exporter en CSV ou en JSON dans un fichier")
    args = parser.parse_args()

    if(args.url):
        userid, token = soundcloud.userid_info(args.url)
        trackslog = soundcloud.listtracks(userid, token)
        #console.print(trackslog)
        listcom = []
        for i in trackslog:
            listcom += soundcloud.listcomments(i, token)


        if(args.biggest_com):
            metricscom = soundcloud.metrics_comments(listcom)
            table = richTable(title="Commentateurs par fréquence")
            table.add_column("Occurences", style="cyan")
            table.add_column("username", style="magenta")
            table.add_column("lien_profile", style="green", no_wrap=True)
            for i in metricscom:
                table.add_row(str(i["nb"]), i["username"], i["link"])
            console.print(table)
        if(args.list_com):
            table = richTable(title="Commentaires")
            table.add_column("texte")
            table.add_column("user")
            table.add_column("lien_profile", style="green", no_wrap=True)
            for i in listcom:
                table.add_row(i['body'], i['user']['username'], i['user']['permalink_url'])
            console.print(table)
        if(args.cloudword):
            # Word tokenization
            from spacy.lang.en import English as spacyEnglish
            from spacy.lang.en.stop_words import STOP_WORDS as spacySTOP_WORDS
            # Load English tokenizer, tagger, parser, NER and word vectors
            nlp = spacyEnglish()
            text = ""
            for i in listcom:
                text += " " + i['body']
            #  "nlp" Object is used to create documents with linguistic annotations.
            doc_NLP = nlp(text)
            del text
            filtered_word = []
            for word in doc_NLP:
                if word.is_stop == False:
                    filtered_word.append(word)
            del doc_NLP
            #print(filtered_word)
            occurence_words = dict()
            for i in filtered_word:
                if(i.text in occurence_words.keys()):
                    occurence_words[i.text] += 1
                else:
                    occurence_words[i.text] = 1
            occurence_words = sorted(occurence_words.items(), key=lambda t: t[1], reverse=True)
            table = richTable(title="Occurences de mots")
            table.add_column("occurence", no_wrap=True)
            table.add_column("mot", no_wrap=True)
            for i in occurence_words:
                table.add_row(str(i[0]), str(i[1]))
            console.print(table)
        if(args.export):
            if(args.export.split('.')[-1] == "json"):
                #export au format JSON
                with open(args.export, 'w') as jsonfile:
                    json.dump(listcom, jsonfile)
            if(args.export.split('.')[-1] == "csv"):
                #export au format CSV
                with open(args.export, 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=listcom[0].keys())
                    writer.writeheader()
                    for com in listcom:
                        writer.writerow(com)
    else:
        console.print("Aucun utilisateur à investiguer")
