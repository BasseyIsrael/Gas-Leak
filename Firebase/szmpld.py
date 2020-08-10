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


    gasr = random.choice(gass)
    tempr = random.choice(temps)
    humr = random.choice(humss)
    doc_ref.add({u'gasconc': gasr, u'temp': tempr, u'hum':humr})
real_time()

while 1<2:
    real_time()
    sleep(20)