#coding:utf-8
"""
+---------------------------------+
|                                 |
|            S3 - P1              |
|                                 |
| DERGHAL Wissem - MOUCHRIT Riyad |
|                                 |
+---------------------------------+
"""
from math import exp, sqrt, pi
import csv
from pylab import plot, title, xlabel, ylabel, xlim, ylim, grid, show, subplot

#49 m d'altitude au laboratoire, le 13/11/2020 à 16h30 il faisait 16°C avec 75% d'humidité
altitude = 49
temperature = 16
humidite = 75

# fonction qui prend en paramètre l’altitude et qui calcule la pression atmosphérique. 
def pression_atmospherique(altitude=49):
    pression = 1013.25 * exp(-(altitude / 8400))
    return round(pression,2)

# fonction qui convertie une température exprimée en degré Celsius en Kelvin. 
def Kelvin(tempC=16):
    tempK = tempC + 273.15
    return tempK

# fonction qui prend en paramètres la température et l’altitude puis qui retourne la pression partielle de vapeur saturante Ps en hecto Pascal. 
def pression_vapeur(temp=16,altitude=49):
    pa = pression_atmospherique(altitude)
    tempK = Kelvin(temp)
    ppvs = pa * exp(13.7 - (5120 / tempK))
    return round(ppvs,2)

# fonction qui prend en paramètres la température, l’altitude, le taux d’humidité relatif et qui retourne la vitesse du son en m/s. 
def vitesse_son(temp=16,altitude=49,humidite=75):
    tempK = Kelvin(temp)
    pv = pression_vapeur(temp,altitude)
    p_air = pression_atmospherique(altitude)
    vs = sqrt(
        (1.4*10**3) * (8.31451 * tempK / 28.965 + ((humidite/100) * (pv/p_air)) * (18.015-28.965))
        )
    return vs

# fonction qui prend en paramètre la température, le taux d’humidité relatif puis l’altitude et qui calcul la masse volumique de l’air. 
def masse_volumique_air(temp=16,altitude=49,humidite=75):
    p_air = pression_atmospherique(altitude) * 100
    p_vap = pression_vapeur(temp,altitude) * 100
    tempK = Kelvin(temp)
    mv = ( p_air-(0.3783 * humidite/100 * p_vap) ) / (287.058 * tempK)
    return round(mv,3)

# fonction qui prend en paramètres les principales caractéristiques associées au projectile, et qui retourne l’énergie cinétique utile en translation ainsi que la vitesse à la bouche du canon en m/s. 
def energie_cinetique(mproj=0.00259,energiemassique=3500,mpoudre=0.14):
    ec = (energiemassique*mpoudre)*0.4  # 40% (energie massique * masse poudre)
    vit = sqrt((ec)/(0.5*mproj))
    return [ec,vit]
    

# fonction qui calcule la densité de section
def densite_section(m,d):
    ds = 1.4223 * (m / d**2)
    return ds

# fonction de lecture CSV qui retourne le coefficient balistique du modèle pour une vitesse donnée
def coeff_balistique_csv(vitesse):
    fichier_coeffs = open("Coefficients.csv","r")
    lecteur = csv.reader(fichier_coeffs, delimiter=";")
    
    colonne1 = []
    colonne2 = []

    for e in lecteur:
        colonne1.append(e[0])
        colonne2.append(e[1])
    
    index = 0
    for i in colonne1:    
        if float(i) == vitesse:
            return colonne2[index]
        index+=1

    fichier_coeffs.close()
    

# fonction qui calcule l'indice de forme i1 en fonction du nombre de Mach
def indice_forme(vitesse_mach):
    i1 = (densite_section(2.59,5.58)) / float(coeff_balistique_csv(vitesse_mach))
    return round(i1,3)

# fonction qui calcul le coefficient balistique CBp1 en fonction du nombre de Mach.
def coeff_balistique(vitesse_mach):
    cb = densite_section(2.59,5.58)/indice_forme(vitesse_mach)
    return cb

# fonction qui prend en paramètre la vitesse initiale, qui calcul la décroissance de la vitesse dvp au bout d’un temps dt = 1 ms, jusqu’à ce que la distance parcourue soit 300 m. 
def decroissance(vitesse_mach=1.1342245191361803869):
    # vitesse initiale en mach 389,0390100637099 : 1,1342245191361803869
    global altitude; global temperature; global humidite
    
    temps = 0.001
    distance = 0
    vitesse = vitesse_mach * vitesse_son(temperature,altitude,humidite)
    liste_t = [0]
    liste_d = []
    liste_v = [vitesse]
    while distance < 300 :
        if vitesse < 292.6:
            a = 0
            b = 0.00093
            c = 0
            d = 0
        elif vitesse > 292.6 and vitesse < 320:
            a = -7.62 * 10e-7
            b = 0.002247
            c = -0.03
            d = 64.019
        elif vitesse > 320:
            a = 0
            b = 0
            c = -0.028
            d = 58.6133
        
        dvp = ((a*(vitesse**3)) + (b*(vitesse**2)) + c*vitesse + d)*0.001
        vitesse = vitesse - dvp
        distance = distance + vitesse/1000
        liste_t.append(temps)
        temps = temps + 0.001
        liste_d.append(dvp)
        liste_v.append(vitesse)
    return [liste_v,liste_t]

def traceMulti():
    liste_v1 = decroissance()[0]
    liste_t = decroissance()[1]
    liste_tt=[]
    for i in range(len(liste_t)):
        liste_tt.append(i)
        
    subplot(221)
    plot(liste_tt,liste_v1,color='b',linestyle='-')
    title('Vitesse en fonction du temps')
    xlabel('temps en ms')
    ylabel('vitesse en m/s')
    xlim(0,max(liste_tt)*1.1)
    ylim(min(liste_v1)*1.01,max(liste_v1)*1.01)
    grid(color='k', linestyle='-', linewidth=0.5)

    liste_c = []
    nbM= [0.5,0.6,0.75,0.8,0.85,0.9,0.925,0.95,0.975,1,1.1,1.25,1.3,1.4,1.5,1.6,1.75,1.8,2,2.2,2.5,3,3.5,4,4.5,5]
    i = nbM[0]
    for i in nbM:
        #print(i)
        liste_c.append(coeff_balistique(i))

    #print(liste_c)
    subplot(222)
    plot(nbM,liste_c,color='m',linestyle='-')
    title('Coefficient balistique en fonction du nombre de Mach ')
    xlabel('Nombre de mach')
    ylabel('Coefficient balistique')
    xlim(0,max(nbM)*1.1)
    ylim(0,max(liste_c)*1.1)
    grid(color='k', linestyle='-', linewidth=0.5)

    liste_v = decroissance()[0]
    liste_t = decroissance()[1]

    liste_e = []
    for i in liste_v:
        liste_e.append(0.5*0.00259*(i**2))
    #print(liste_e)
    
    subplot(223)
    plot(liste_tt,liste_e,color='r',linestyle='-')
    title('Energie cinétique en fonction du temps')
    xlabel('Temps en ms')
    ylabel('energie cinétique en J')
    xlim(min(liste_tt),max(liste_tt)*1.05)
    ylim(min(liste_e),max(liste_e)*1.005)
    grid(color='k', linestyle='-', linewidth=0.5)
    show()

def csv_final():

    vitesse_initiale = 389.0390100637099

    table = []

    liste_v = decroissance()[0]
    liste_t = decroissance()[1]
    liste_tt = []


    for i in liste_t :
        i = i * 1000
        liste_tt.append(int(i))

    for i in range(0,len(liste_v)):
        table.append([])
        table[i].append(liste_v[i])
        table[i].append(liste_tt[i])

    
    with open('csv_final.csv', 'w', newline='') as csvfinal:
        writer = csv.writer(csvfinal, delimiter =',')

        writer.writerow(("Vitesse initiale :",vitesse_initiale))
        writer.writerow(("Vitesse en m/s","Temps en ms","Distance en m"))



#print(pression_atmospherique(49))
#print(Kelvin(16))
#print(pression_vapeur(16,49))
#print(vitesse_son(16,49,75))
#print(masse_volumique_air())
#print(energie_cinetique())
#print(densite_section(2.59,5.58))
#print(coeff_balistique_csv(1))
print(decroissance())
#print(coeff_balistique(0.5))#print(indice_forme(1))
#print(decroissance(5))
#traceMulti()
#csv_final()