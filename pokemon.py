import pandas as pd
import random

pokemonDf = pd.read_csv("pokemon.csv")
pokemonDf = pokemonDf.dropna()

comuniDf = pokemonDf[pokemonDf['Rarità'] == 'Comune']
nonComuniDf = pokemonDf[pokemonDf['Rarità'] == 'Non Comune']
rariDf = pokemonDf[pokemonDf['Rarità'] == 'Rara']
ultraRariDf = pokemonDf[pokemonDf['Rarità'] == 'Ultra Rara']

collezione = []

crediti = 100

def apriPacchetto():
    if (crediti >= 10):
        for i in range(5):
            estraiCarta()
    else:
        print("Non hai abbastanza crediti!")

def mostraCollezione ():
    if len(collezione) == 0:
        print("Collezione vuota!")
    else:
        for i in range(len(collezione)):
            print(collezione[i])

def mostraPunti ():
    print(f"I tuoi punti sono: ", crediti)

def salvaCollezione ():
    if len(collezione) == 0:
        print("Collezione vuota! Niente da salvare.")
    else:
        collezioneDf = pd.concat(collezione, ignore_index=True)
        collezioneDf.to_csv("collezione.csv", index=False)
        print("Collezione salvata con successo!")

def estraiCarta():
    rand = random.randint(0,100)
    try:
        if (rand <= 70):
            estratto = comuniDf.sample()
        elif (rand > 70 and rand <= 90):
            estratto = nonComuniDf.sample()
        elif (rand > 90 and rand <= 99):
            estratto = rariDf.sample()
        elif (rand > 99):
            estratto = ultraRariDf.sample()
        print(estratto)
        collezione.append(estratto)
    except:
        print("Errore durante l'estrazione della carta.")

print("Benvenuto nel gioco dei Pokemon!")
print("1. Apri pacchetto")
print("2. Mostra collezione")
print("3. Mostra punti")
print("4. Salva collezione")
print("0. Esci")
x = int(input("Seleziona un opzione (1-4):"))

while x != 0:
    if (x == 1):
        apriPacchetto()
        crediti -= 10
    elif (x == 2):
        mostraCollezione()
    elif (x == 3):
        mostraPunti()
    elif (x == 4):
        salvaCollezione()
    x = int(input("Seleziona un opzione (1-4):"))

print("Alla prossima!")