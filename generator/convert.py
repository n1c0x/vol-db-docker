import json
import csv
import pprint

json_data_list = []
json_data_dict = {}
pk = 1

with open('iata_beautify.json') as f:
    data = json.load(f)
    for choses in data:
        for key, values in choses.items():
            # print("clé : "+key+" valeur : "+values)
            if choses["type"] == "medium_airport":
                json_data_dict = {"model": "vol.codeiata"}
                json_data_dict = {"pk": pk}
                # json_data_dict = {"fields"} = {}
                if key == "iata_code":
                    # print("Code IATA: "+values)
                    json_data_dict = {"fields": {"code_iata": values}}
                elif key == "name":
                    # print("Ville: "+values)
                    json_data_dict = {"fields": {"ville": values}}
                print(json_data_dict)
        pk = pk + 1

print(json_data_dict)
