def fullcsv(mach=2.5) :                 # Création d'un csv dans lequel on a seulement les données en fonction du mach que l'on indique
    liste = []        # Liste qui va représenter le tableau que l'on va ajouter au csv
    v = decroiss()[0]      # liste_v contient toutes les vitesses sur 300 m
    t = decroiss()[2]
    tt = []
    d = decroiss()[1]       # liste_d contient toutes les distances en m par ms sur 300
    for i in t :
        i = i * 1000
        tt.append(int(i))                         # liste_tt contient les temps en ms sur 300 m
        
    for i in range(0,len(v)):
        liste.append([])
        liste[i].append(v[i])
        liste[i].append(tt[i])
        liste[i].append(d[i])

    liste.append([])
    liste[len(tt)].append('Pression atmospherique')
    liste[len(tt)].append(patmos(altitude))
    liste.append([])
    liste[len(tt) + 1].append('Température en kelvin')
    liste[len(tt) + 1].append(c_to_k(temperature))
    liste.append([])
    liste[len(tt) + 2].append('Pression partielle de vapeur saturante')
    liste[len(tt) + 2].append(patmos_partielle(altitude,temperature))
    liste.append([])
    liste[len(tt) + 3].append('Vitesse du son')
    liste[len(tt) + 3].append(vitesse_son(altitude,temperature,hr))
    liste.append([])
    liste[len(tt) + 4].append("Masse volumique de l'air")
    liste[len(tt) + 4].append(masse_vol(altitude,temperature,hr))
    liste.append([])
    liste[len(tt) + 5].append('Energie cinetique')
    liste[len(tt) + 5].append(energieutile(masspoudre,massproj)[0])
    liste.append([])
    liste[len(tt) + 6].append('Vitesse du projectile')
    liste[len(tt) + 6].append(energieutile(masspoudre,massproj)[1])
    liste.append([])
    liste[len(tt) + 7].append('Densite de section')
    liste[len(tt) + 7].append(densection(massproj,diamproj))
    liste.append([])
    liste[len(tt) + 8].append('Indice de forme')
    liste[len(tt) + 8].append(indiceforme(mach))
    liste.append([])
    liste[len(tt) + 9].append('Coefficient balistique')
    liste[len(tt) + 9].append(coeff_bal(mach))

    with open('../csv/CSV AIT ALLA IREZIEV.csv','w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter =',')
        
        writer.writerow(("Mach :", mach, ""))
        writer.writerow(("Vitesse en m/s","Temps en ms","Distance en m"))
        try :
            for l in range(len(tt)) :
                writer.writerow((liste[l][0],liste[l][1],liste[l][2]))
            writer.writerow(("","",""))

            for i in range(len(tt),len(tt) + 10) :
                writer.writerow((liste[i][0],liste[i][1]))
        except :
            None