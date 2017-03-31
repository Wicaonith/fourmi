#! /usr/bin/env python
# -*- coding: Utf-8 -*-

import csv
import random
import datetime
import networkx as nx

###########################################
############## CONSTANTES #################
###########################################

CONST_COMMUNE = "COMMUNE"
CONST_TENANT = "TENANT"
CONST_ABOUTISSANT = "ABOUTISSANT"
CONST_BI_MAX = "BI_MAX"
CONST_LIBELLE = "LIBELLE"

CONST_START = "NANTES Rue Alfred Nobel"
CONST_END = "NANTES Rue du Pontereau"
#"NANTES Rue Maréchal Joffre"
CONST_ANT_COUNT = 5
CONST_GENERATION_COUNT = 1


# Methode "main"
def init():
    # Generation du graphe
    graph = csvToGraph()
    
    # Generation du tableau associatif des aretes avec un index
    streetIndexTab = generateStreetIndex(graph)
    
    for generation in range(CONST_GENERATION_COUNT):
        
        # On envoit plusieurs fourmis
        for i in range(CONST_ANT_COUNT):

            print("Fourmi numero " + str(i+1))

            # Generation d'une nouvelle fourmi
            ant = generateAnt(generation)
            # on l'envoie se promener sur la carte 

            print("Départ d'une fourmi")

            #d=datetime.timedelta()
            #timeStart = datetime.datetime.now().time();
            # On envoi une fourmi sur le trajet
            ant = walk(graph, streetIndexTab, ant)
            print("Arrivé d'une fourmi")
            #timeEnd = datetime.datetime.now().time();
            print(" ")
            print("Chemin Parcouru: ")
            print(ant["waythrough"])
            print(" ")
            print("Nombre de rues parcourues: ") #+ ant["waythrough"]
            #print("Durée: " + (timeEnd - timeStart))
            print("Gestion des phéromones")
            # La on va poser les petites pheromones de chaques fourmies
            graph = pheromoneDrop(graph, ant)
            # la on enleve un ptit peu de pheromone
            graph = pheromoneMiss(graph)

# Transforme le CSV contenant les données de la ville de Nantes en graphe 
# pour créer des chemin pour les fourmis.
def csvToGraph(): 
    # Ouvrir
    with open('VOIES_NM.csv', 'r', encoding='UTF8') as csvfile:
        readCSV = csv.DictReader(csvfile, delimiter=',')

        graph = nx.Graph()
        i = 0

        # On boucle sur chaque rue présente dans le CSV
        for street in readCSV:
            # 
            nextStreet = street[CONST_COMMUNE] + " " + street[CONST_LIBELLE]

            if(street[CONST_TENANT] != '' and street[CONST_ABOUTISSANT] != ''):
                # Si impasse
                if(street[CONST_TENANT] != '' and street[CONST_ABOUTISSANT] == "Impasse"):
                    graph.add_edge(street[CONST_TENANT], street[CONST_COMMUNE] + " " + str(i), street=nextStreet, weight=street[CONST_BI_MAX], phero=0)
                else:
                    graph.add_edge(street[CONST_TENANT], street[CONST_ABOUTISSANT], street=nextStreet, weight=street[CONST_BI_MAX], phero=0)
                    # Si ni tenant ni abouttisant
            elif(street[CONST_TENANT] != '' and street[CONST_ABOUTISSANT] == ''):
                graph.add_edge(street[CONST_TENANT], street[CONST_COMMUNE] +" "+ str(i), street=nextStreet, weight=street[CONST_BI_MAX], phero=0)
            elif(street[CONST_TENANT] == '' and street[CONST_ABOUTISSANT] != ''):
                graph.add_edge(street[CONST_COMMUNE] +" "+ str(i), street[CONST_ABOUTISSANT], street=nextStreet, weight=street[CONST_BI_MAX], phero=0)
            elif(street[CONST_TENANT] == '' and street[CONST_ABOUTISSANT] == ''):
                graph.add_edge(street[CONST_COMMUNE] + " " + str(i), street[CONST_COMMUNE] +" "+ str(i + 1), street=nextStreet, weight=street[CONST_BI_MAX], phero=0)
                i = i + 1
            i = i + 1

        return graph


# Generation du dictionnaire des rues
# Un index est lié à une rue pour facilité les calculs
def generateStreetIndex(graph):
    i = 0
    tab = {}

    for street in list(graph.edges_iter(data="street")):
        tmp = street[2]["street"]
        tab[tmp] = i
        i = i + 1

    return tab


# Création d'une fourmi avec pour caractéristiques
#   Le nom
#   Le poids par rapport a la distance parcouru
#   Le départ
#   L'arrivé
#   Les rues visitées
def generateAnt(i):
    name = "Ant" + str(i)
    ant = {}

    ant["name"] = name
    ant["distance"] = 0
    ant["start"] = CONST_START
    ant["end"] = CONST_END
    #Dictionnaire des rues visitées
    ant["waythrough"] = {}
    ant["real_waythrough"] = {}

    return ant

# On envoit la fourmi sur le chemin
def walk(graph, streetIndexTab, ant):

    # Initialisation du départ de la fin du graphe
    start = ant['start']
    end = ant['end']

    # On regarde dans la tableau pour la rue de depart
    index = streetIndexTab[start]
    currentStreet = "Une rue qui ne doit pas exister pour l'initialisation"

    # La fourmi continue tant qu'on a pas trouver la destination
    while(end != currentStreet):

        # On choisi aléatoirement un noeud où la fourmi va se rendre
        # Recupération du noeud
        if(random.randint(0,1) == 1):
            node = graph.edges()[index][0]
        else:
            node = graph.edges()[index][1]

        # On choisi aléatoirement un chemin possible qui part du node choisi
        choice = choiceWay(graph.edges(node, data='street'))

        currentStreet = graph.edges(node, data='street')[choice][2]['street']

        index = streetIndexTab[currentStreet]
        
        # Si la rue est déjà visité, on en choisi une autre
        if(index in ant["waythrough"]):
            unseenStreet = []
            # Vérification des rues restantes en fonction des rues déjà passées.
            for mesReste in graph.edges(node, data='street'):
                indextempo = streetIndexTab[mesReste[2]['street']]
                if(indextempo in ant["waythrough"]):
                    unseenStreet.append(mesReste)

            # Si il reste des choix on randomise sur celle ci
            if(len(unseenStreet)>0):
                choice = choiceWay(graph.edges(unseenStreet[0][0], data='street'))
                currentStreet = graph.edges(node, data='street')[choice][2]['street']
                index = streetIndexTab[currentStreet]

        #Si l'index choisi n'est pas encore passer par notre fourmi ont continue
        #On ajoute nos waythrough dans un dictionnaire liée a une fourmie
        ant["waythrough"][index] = index
        ant["real_waythrough"][index] = index
        if(graph.edges(node, data='street')[choice][2]['weight'] != ''):
            ant["distance"] = ant["distance"] + (int(graph.edges(node, data='street')[choice][2]['weight'])*0.01)
        
    if(end == currentStreet):

        return ant

# Depuis un noeuds il peut y avoir plusieurs possibilité
# Notation des rues par rapport aux phéromones
def choiceWay(nodes):
    # Cela sera la valeur max du random a faire
    totalRank = 0

    # nombre de choix possible
    nbChoix = len(nodes)
    
    # proportion sur 100 par le nombre de choix
    rank = 100/nbChoix

    rangePossible = []
    for node in nodes:
        # on ajoute les pheromones
        if(node[2]['phero'] > 0):
            rangePossible.append(rank + node[2]['phero'])
            totalRank = totalRank + rank + node[2]['phero']
        else:
            # sinon on prend la rank normal
            rangePossible.append(rank)
            totalRank = totalRank + rank

    # On randomise sur tous ca
    monRAN = random.randint(0, round(totalRank))
    
    # Index du tableau et index du noeud choisie
    i = 0
    mini = 0
    maxi = 0
    for test in rangePossible:
        maxi = maxi + test
        if(monRAN >= mini and monRAN <= maxi):
            return i
        i = i + 1
        mini = mini + test
        # return 0 pour au cas ou si sa bug
    return 0


# Méthode qui permet d'ajouter des phéromones sur le chemin parcouru par la fourmi
# On fait une fonction de fitness sur le tableau des rues où la fourmi est déjà passé
def pheromoneDrop(graph, ant):

    # Rues connues
    way = ant["waythrough"]
    for i in way:
        ret = 0
        if(ant["distance"] > 1):
            # Inversement de la distance
            phero =  1 / ant["distance"]
            # On ne garde que ce qu'il y a à droite de la virgule
            phero = str(phero).split('.')
            for j in phero[1]:
                if(j == '0'):
                    ret = ret + 10
                else:
                    ret = ret + int(j)
                    break
            # Inversion
            if(ret <= 100):
                ret = 100 - ret
            else:
                ret = 0

        graph.edges(data='phero')[i][2]['phero'] = graph.edges(data='phero')[i][2]['phero'] + ret

    return graph


# Enleve 5% des pheromones chaque generation 
def pheromoneMiss(graph):

    for i in range(len(graph.edges())):
        if(graph.edges(data='phero')[i][2]['phero'] > 0):
            graph.edges(data='phero')[i][2]['phero'] = round(graph.edges(data='phero')[i][2]['phero'] - (graph.edges(data='phero')[i][2]['phero'] * 0.05))
    return graph




