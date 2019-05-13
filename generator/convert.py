import json
import csv
import pprint

'''
# Open the CSV  
f = open( 'iata.csv', 'rU' )  
# Change each fieldname to the appropriate field name. I know, so difficult.  
reader = csv.DictReader( f, fieldnames = ( "ident","type","name","elevation_ft","continent","iso_country","iso_region","municipality","gps_code","iata_code","local_code","coordinates" ))  
# Parse the CSV into JSON  
out = json.dumps( [ row for row in reader ] )  
print("JSON parsed!")  
# Save the JSON  
f = open( 'data.json', 'w')  
f.write(out)  
print("JSON saved!")'''

json_data_list = []
json_data_dict = {}
pk = 1

with open('iata_beautify.json') as f:
    data = json.load(f)
    for choses in data:
        for key,values in choses.items():
            #print("clé : "+key+" valeur : "+values)
            if choses["type"] == "medium_airport":
                json_data_dict = {"model":"vol.codeiata"}
                json_data_dict = {"pk": pk}
                #json_data_dict = {"fields"} = {}
                if key == "iata_code":
                    #print("Code IATA: "+values)
                    json_data_dict = {"fields":{"code_iata": values}}
                elif key == "name":
                    #print("Ville: "+values)
                    json_data_dict = {"fields":{"ville": values}}
                print(json_data_dict)
        pk = pk + 1

print(json_data_dict)
