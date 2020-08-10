import csv
from time import sleep
import random
import pandas as pd
import itertools

import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./energy-challenge-firebase-adminsdk-qma15-45f970d8c2.json")
app = firebase_admin.initialize_app(cred)

def real_time():
    store = firestore.client()
    doc_ref = store.collection(u'users').limit(2)

    doc_ref = store.collection(u'Gas Leak Data New')

    dataset = pd.read_csv("Sensor.csv")
    print(dataset.head)

    timee = []
    gass = []
    temps = []
    humss = []
    for row in dataset.itertuples():
        tim = row.Time
        gas = row.Concentration
        temp = row.TemperatureC
        hums = row.Humidity
        timee.append(tim)
        gass.append(gas)
        temps.append(temp)
        humss.append(hums)

    #gasconc = dataset.gasconc
    #tempdegc = dataset.tempdegc
    #hum = dataset.hum

    #print (gasconc)

    #for i in gasconc:
     #   gas.append(i)

    #for x in tempdegc:
     #   temp.append(x)
    #for m in hum:
     #   hums.append(m)

    #print(gas)
    #print(temp)
    #print(hums)




    #with open(dataset, 'r') as fh:
        #reader = csv.reader(fh)
        #for column in reader:
         #   gasconc = [int(value)for value in column(0)]

            # list comprehension for float conversion
           # tempdegC, hum = [float(value) for value in column[1:]]
           # gas.append(gasconc)
          #  temp.append(tempdegC)
         #   hums.append(hum)
    for (d,g,t,h) in itertools.zip_longest(timee, gass, temps,humss):
        timer = d
        gasr = g
        tempr = t
        humr = h
        doc_ref.add({u'Gas concentration': gasr, u'Temperature': tempr, u'Humidity': humr,u'Time': timer})
        sleep(20)
    #gasr = random.choice(gass)
    #tempr = random.choice(temps)
    #humr = random.choice(humss)
    #doc_ref.add({u'gasconc': gasr, u'temp': tempr, u'hum':humr})
real_time()

while 1<2:
    real_time()
    sleep(5)