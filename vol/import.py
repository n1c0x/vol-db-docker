# open file & create csv reader
import csv

# import the relevant model
#from .models import Vol

# loop
with open ('../../cdv2013.csv',newline='') as csvfile:
    spamreader = csv.reader(csvfile,delimiter=';')
    for row in spamreader:
        #print(', '.join(row))
        date = row[0]
        cdb = row[1]
        opl = row[2]
        obs1 = row[3]
        obs2 = row[4]
        instructeur = row[5]
        depart = row[6].split("/")[0]
        arrivee = row[6].split("/")[1]
        jour = row[7]
        nuit = row[8]
        ifr = row[9]
        arrivee_ifr = row[10]
        fonction = row[11]
        immatriculation = row[12]
        type_avion = row[13]
        observation = row[14]
        poste = row[15]
        