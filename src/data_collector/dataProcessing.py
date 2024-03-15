import json
from data_collector.webScraper import *

###################################################
#         JSON file generator from data           #
###################################################

def generate_json(data : str, json_text : str):
    splited_data = data.split(">")
    clean_data = splited_data[0]
    # Crée un objet BeautifulSoup pour analyser le contenu HTML
    soup = BeautifulSoup(json_text, 'html.parser')

    # Trouve la balise <CODE> et extrait son contenu
    code_bal = soup.find('code')
    #print(code_bal.text)

    #Trie des lignes et préparation du format JSON
    JSON_new = {}
    JSON_new["type_noeud"] = {}
    JSON_new["noeud"] = {}
    JSON_new["type_relation"] = {}
    JSON_new["relation"] = {}
    lines = code_bal.text.split('\n')
    for line in lines:
        line_dict = {}
        attributes = line.split(';')

        if line.startswith('nt;'):
            line_dict["ntname"] = str(attributes[2].replace("'", ""))
            JSON_new["type_noeud"][attributes[1]] = line_dict

        if line.startswith('e;') and not(attributes[2].startswith("'_")):
            line_dict["name"] = str(attributes[2].replace("'", ""))
            line_dict["w"] = str(attributes[4])
            try:
                line_dict["formated name"] = str(attributes[5])
            except IndexError as e:
                line_dict["formated name"] = None
            JSON_new["noeud"][attributes[1]] = line_dict

        if line.startswith('rt;'):
            line_dict["trname"] = str(attributes[2].replace("'", ""))
            line_dict["trgpname"] = str(attributes[3].replace("'", ""))
            JSON_new["type_relation"][attributes[1]] = line_dict

        if line.startswith('r;'):
            line_dict["node1"] = int(attributes[2])
            line_dict["node2"] = int(attributes[3])
            line_dict["type"] = int(attributes[4])
            line_dict["w"] = int(attributes[5])
            try:
                if(attributes[6] == ' - ' or attributes[6] == '-'):
                    line_dict["wnormed"] = None
                else:
                    line_dict["wnormed"] = float(attributes[6])
            except IndexError as e:
                line_dict["wnormed"] = None
            try:
                if(attributes[7] == ' - ' or attributes[7] == '-'):
                    line_dict["rank"] = None
                else:
                    line_dict["rank"] = int(attributes[7])
            except IndexError as e:
                line_dict["rank"] = None
            JSON_new["relation"][attributes[1]] = line_dict
    
    # Écrire le fichier JSON
    with open('data/'+clean_data+'.json', 'w', encoding='utf-8') as json_file:
        json.dump(JSON_new, json_file, ensure_ascii=False, indent=4)

###################################################
#           Main test function                    #
###################################################

def processData(data : str = ""):
    #text = input("donnee a recuperer : ")
    if(not(data_already_acquired(data))):
        print("Acquisition de nouvelles données...")
        reponse = http_request(data)
        generate_json(data, reponse)
        return True
    else:
        return False