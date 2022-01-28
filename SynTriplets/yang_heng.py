import pathlib
from gensim.models import KeyedVectors as kv
import spacy
from scipy.stats import hmean
import json


# chemin vers le fichier des plongement lexicaux
embfile = "./frWac_non_lem_no_postag_no_phrase_200_skip_cut100.bin"

# Charger les plongements lexicaux en mémoire
wv = kv.load_word2vec_format(embfile, binary=True, encoding='UTF-8', unicode_errors='ignore')

# Charger spacy avec le modèle du français
spacy_nlp = spacy.load('fr_core_news_md')


# Pour chacun des trois aspects, on fournit des mots-exemples qui seront utilisés pour calculer
# des scores de similarité avec chaque token du texte afin de décider s'il exprime un des
# trois aspects
aspects = {
    'nourriture': ['dessert', 'poisson', 'riz', 'pâtes', 'purée', 'viande', 'sandwich', 'frites'],
    'boisson': ['eau', 'vin', 'limonade', 'bière', 'jus', 'thé', 'café'],
    'service': ["service", 'serveur', 'patron', 'employé'],
}


# Similarité moyenne entre un mot et un ensemble de mots : on prend la moyenne harmonique des distances
# puis on la soustrait à 1 pour obtenir la mesure inverse (la similarité), et on arrondit à 4 décimales.
def get_sim(word, other_words):
    if word not in wv.key_to_index:
        return 0
    dpos = wv.distances(word, other_words)
    d = hmean(abs(dpos))
    return round((1 - d),4)


# Pour un token spacy, cette méthode décide si c'est un terme d'aspect en cherchant l'aspect pour
# lequel il a une similarité maximale (calculée avec les mots-exemples des aspetcs).
# si le score maxi est plus petit que 0.5, il n'y pas d'aspect et la méthode retourne None
def get_aspect_emb(token):
    if token.pos_ != "NOUN":
        return None
    aspect_names = [aspect_name for aspect_name in aspects]
    scores = [(aspect_name,get_sim(token.lemma_, aspects[aspect_name])) for aspect_name in aspect_names]
    scores.sort(key=lambda x:-x[1])
    max_score = scores[0][1]
    max_aspect = scores[0][0] if max_score >= 0.5 else None
    return max_aspect


######################################################################################################
# Ne pas modifier le code ci-dessus
# Rajoutez votre code d'extractions après ce commentaire
# vous devez utiliser la méthode get_aspect_emb(token) définie ci-dessus pour savoir si un token
# est un terme d'aspect et (quel aspect)
######################################################################################################
import sys

advmod_neg = {'pas', 'non', 'peu', 'guère', 'mal', 'trop'}
currentPath = pathlib.Path.cwd()

def get_textes():
    """Chargement des textes dans une liste.

    Obtenir le nom du fichier{file_name} de texte à partir du répertoire principal du projet
    avec des arguments de ligne de commande, afficher les contenus du fichier
    et sauvegarder les textes dans la liste{textes_list}.

    Returns:
        textes_list (list): Cette liste contient les textes à analyser avec spaCy.
    """
    
    file_name = sys.argv[1]
    file_path = currentPath.joinpath(pathlib.Path(file_name))
    try:
        if pathlib.Path(file_path).exists:
            with file_path.open('r',encoding='utf-8') as f:
                textes_list = [] # Initialiser la liste
                for line in f.readlines():
                    # chargement des textes dans une liste sans '\n'
                    textes_list.append(line.strip())
            # print(textes_list)
            print(f"Contenu du fichier de {file_name} en entrée:")
            print("=====================================>")
            for texte in textes_list:
                print(texte)
            return textes_list
    except IOError: 
        print(f"The file =>{file_path}<= does not exist, exiting...")

def mk_file_json(resultats):
    """Sauvegarder les résultats au format json dans un fichier de sortie nommé resultats.json

    Args:
        resultats (json): Une liste qui contient les résultats 
        des triplets extraits regroupés avec leur phrase d’origine.
    """    

    json_file = pathlib.Path("resultats.json")
    json_file.touch()
    file_out_path = currentPath.joinpath(json_file)
    try:
        if pathlib.Path(file_out_path).exists:
            with file_out_path.open('w',encoding = 'utf-8') as rj:
                rj.write(resultats)

            # Affichage les contenus du fichier json
            contenu_json = file_out_path.read_text()
            print("==================================================")
            print(f"Contenu du fichier {json_file} (au format json):\n{contenu_json}")
    except IOError: 
        print(f"The json file =>{file_out_path}<= does not exist, exiting...")




# ! Les contraintes syntaxiques suivantes

# * Contraintes 1
def is_contrainte_1(token):
    """Contraintes 1 : Le terme d’aspect t doit être 
    un nom commun (catégorie grammaticale NOUN de UD2)

    Args:
        token (Token object de spaCy): un terme d'aspect

    Returns:
        (boolean): Si le terme d'aspect t est un nom commun, la fonction renvoie Vrai
    """
    if token.pos_ == "NOUN":
        return True

# * Contraintes 2 : L’expression c est soit (a),(b),(c),(d)
def contrainte_2abc(token):
    """Contraintes 2a 2b 2c 
    
    On cherche si ce terme remplit une des contraintes concernant la caractérisation 2a 2b 2c.

    Args:
        token (Token object de spaCy): 
        un terme d'aspect avec la contrainte 1 satisfaite

    Returns:
        1. expression_a ou expression_b (str):
        La contrainte 2a ou 2b est satisfaite et on identifie 
        {expression_a} ou {expression_b) comme une caractérisation du terme d’aspect.
        
        2. expression_a, a2 ou expression_b, b2 (tuple):
        La contrainte (2a, 2c) ou (2b, 2c) sont satisfaites et on identifie 
        {expression_a, a2} ou {expression_b, b2) comme caractérisations du terme d’aspect.
    """    
    try:
        # vérifier si contrainte 2b
        if token.dep_ == "nsubj" and token.head.pos_ == "ADJ":
            expression_b = token.head
            # vérifier si contrainte 2c
            b2 = contrainte_2c(expression_b)
            if not b2:
                return expression_b # 1 2b
            else:
                return expression_b, b2 # 1 2b 2c

        # vérifier si contrainte 2a
        else:
            for token_child in token.children:
                if token_child.dep_ == "amod" and token_child.pos_ == "ADJ":
                    expression_a = token_child
                    # vérifier si contrainte 2c
                    a2 = contrainte_2c(expression_a)
                    if not a2:
                        return expression_a # 1 2a
                    else:
                        return expression_a, a2 # 1 2a 2c
    except Exception as result:
        print(result)


def contrainte_2c(token_expression):
    """Contraintes 2c

    On vérifie la contrainte 2c pour les cas de coordination

    Args:
        token_expression (Token object de spaCy):
        expression avec la contrainte 2a ou 2b satisfaite

    Returns:
        expression_co (Token object de spaCy):
        une autre caractérisation du terme de l'aspect
    """    
    for token_expression_child in token_expression.children:
        if token_expression_child.dep_ == "conj" and token_expression_child.pos_ == "ADJ":
            expression_co = token_expression_child
            return expression_co

def contrainte_2d(expression):
    """Contraintes 2d
    
    On vérifie la contrainte du modifieur négatif
    et on préfixe {expression} avec le modifieur négatif,
    pour obtenir {neg_expression} comme la caractérisation du terme.

    Args:
        expression (Token object de spaCy): valeur de retour de la function contrainte_2abc

    Returns:
        1. expression_list (list):
        Deux caractérisations du term de l'aspect

        2. expression (str):
        Une caractérisation du term de l'aspect

    """    
    try:
        if expression != None:
            if type(expression) == tuple:
                expression_list = []
                # expression = list(expression)
                for c in expression:
                    # print(c.text,c.pos_)
                    for mod_expression in c.children:
                        if mod_expression.dep_ == "advmod" and mod_expression.text in advmod_neg:
                            c = mod_expression.text + "_" + mod_expression.head.text
                    if type(c) != str:
                        c = c.text
                    expression_list.append(c)
                    # print(expression_list)
                return expression_list
            else:
                # print(c.text,c.pos_)
                # print(type(expression))
                for mod_expression in expression.children:
                    if mod_expression.dep_ == "advmod" and mod_expression.text in advmod_neg:
                        expression = mod_expression.text + "_" + mod_expression.head.text
                if type(expression) != str:
                    expression = expression.text
                # print(expression,type(expression))
                return expression
    except Exception as result:
        print(result)

def ajout_triplet(expression_s):    
    """On extrait ainsi le triplet et on le rajoute à la liste triplets

    Args:
        expression_s (list ou str): La valeur de retour de la fonction contrainte_2d 
    """    
    try:
        if type(expression_s) == list:
            for c in expression_s:
                triplet = [aspect, term, c]
                triplets.append(triplet)
        elif type(expression_s) == str:
            triplet = [aspect, term, expression_s]
            triplets.append(triplet)
        else:
            triplet = "pas d’extraction"
            triplets.append(triplet)
    except Exception as result:
        print(result)

textes = get_textes() # Récupérer les textes à analyser

docs = spacy_nlp.pipe(textes) # analyse des textes avec spaCy

resultats = [] # liste globale des résultats par phrase
for doc in docs:
    # pour chaque document 'doc'
    for sent in doc.sents:
        # pour chaque phrase 'sent' de 'doc', extraires les triplets, s'il y en a,
        # et les stocker dans une liste initialement vide
        triplets = []
        for token in sent:

            # print('{0}({1}) <-- {2} -- {3}({4})'.format(token.text, token.pos_, token.dep_, token.head.text, token.head.pos_))

            # pour chaque token de la pharse, on vérifie si c'est un terme d'aspect
            aspect = get_aspect_emb(token) # méthode fournie dans le code initial
            if aspect is not None:
                term = token.text
            # si c'est un terme d'aspect, on cherche si les contraintes syntaxiques
            # d'extraction sont satisfaites et on crée éventuellement des triplets
            # (aspect, term, c) qu'on rajoute à la liste triplets

                # ! Vérifier les contraintes syntaxiques
                if is_contrainte_1(token):
                    c = contrainte_2abc(token)
                    c = contrainte_2d(c)

                    ajout_triplet(c)
                else:
                    triplet = "pas d’extraction: car le terme n'est pas un nom commun (NOUN)"
                    triplets.append(triplet)

        # sauvegarde du résultat pour cette phrase
        resultat = {'phrase': sent.text, 'triplets': triplets}
        resultats.append(resultat)

# ! Sauvegarder les résultats au format json dans un fichier de sortie nommé resultats.json
resultats_json = json.dumps(resultats, sort_keys=True, indent=4,ensure_ascii=False)
mk_file_json(resultats_json)

