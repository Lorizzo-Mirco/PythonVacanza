import pandas as pd
import random
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "pokemon_app_secret_key"

pokemonDf = pd.read_csv("pokemon.csv")
pokemonDf = pokemonDf.dropna()

comuniDf = pokemonDf[pokemonDf['Rarità'] == 'Comune']
nonComuniDf = pokemonDf[pokemonDf['Rarità'] == 'Non Comune']
rariDf = pokemonDf[pokemonDf['Rarità'] == 'Rara']
ultraRariDf = pokemonDf[pokemonDf['Rarità'] == 'Ultra Rara']

collezione = []

crediti = 100

@app.route('/')
def index():
    return render_template('index.html', crediti=crediti, collezione=collezione)

@app.route('/apri_pacchetto', methods=['POST'])
def apriPacchetto():
    global crediti
    if crediti >= 10:
        crediti -= 10
        carte_estratte = []
        for i in range(5):
            carta = estraiCarta()
            if carta is not None:
                carte_estratte.append(carta)
        flash("Hai aperto un pacchetto e hai ottenuto 5 carte!")
        return render_template('pacchetto.html', carte=carte_estratte, crediti=crediti)
    else:
        flash("Non hai abbastanza crediti!")
        return redirect(url_for('index'))

@app.route('/mostra_collezione', methods=['GET'])
def mostraCollezione():
    if len(collezione) == 0:
        flash("Collezione vuota!")
        return redirect(url_for('index'))
    else:
        return render_template('collezione.html', collezione=collezione, crediti=crediti)

@app.route('/mostra_punti', methods=['GET'])
def mostraPunti():
    return render_template('punti.html', crediti=crediti)

@app.route('/salva_collezione', methods=['POST'])
def salvaCollezione():
    if len(collezione) == 0:
        flash("Collezione vuota! Niente da salvare.")
    else:
        try:
            collezioneDf = pd.concat(collezione, ignore_index=True)
            collezioneDf.to_csv("collezione.csv", index=False)
            flash("Collezione salvata con successo!")
        except Exception as e:
            flash(f"Errore durante il salvataggio: {str(e)}")
    return redirect(url_for('index'))

def estraiCarta():
    rand = random.randint(0,100)
    try:
        if rand <= 70:
            estratto = comuniDf.sample()
        elif rand > 70 and rand <= 90:
            estratto = nonComuniDf.sample()
        elif rand > 90 and rand <= 99:
            estratto = rariDf.sample()
        elif rand > 99:
            estratto = ultraRariDf.sample()
        collezione.append(estratto)
        return estratto
    except Exception as e:
        flash(f"Errore durante l'estrazione della carta: {str(e)}")
        return None

if __name__ == '__main__':
    app.run(debug=True)

