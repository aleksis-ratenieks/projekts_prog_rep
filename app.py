from flask import Flask, render_template, redirect, url_for, request, flash
from models.models import db, Dators, Skolotajs, Lietojums
from config import Config
from utils.external_api import get_weather_info
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def setup_db():
    """Izveido datubāzes tabulas un pievieno sākuma datus, ja tās ir tukšas."""
    db.create_all()

    # Pārbauda, vai datubāzē jau ir dati
    if not Dators.query.first():
        dators1 = Dators(nosaukums='Chromebook 1')
        dators2 = Dators(nosaukums='Chromebook 2')
        dators3 = Dators(nosaukums='Chromebook 3')

        skolotajs1 = Skolotajs(vards='Anna', uzvards='Ozola', epasts='anna@skola.lv')
        skolotajs2 = Skolotajs(vards='Jānis', uzvards='Kalns', epasts='janis@skola.lv')
        skolotajs3 = Skolotajs(vards='Marta', uzvards='Liepa', epasts='marta@skola.lv')

        db.session.add_all([dators1, dators2, dators3, skolotajs1, skolotajs2, skolotajs3])
        db.session.commit()


@app.route('/')
def index():
    """Sākumlapa — parāda datoru sarakstu un temperatūru."""
    datori = Dators.query.all()
    skolotaji = Skolotajs.query.all()
    laikapst = get_weather_info()
    return render_template('index.html', datori=datori, skolotaji=skolotaji, laikapst=laikapst)


@app.route('/datori')
def datoru_saraksts():
    """Visu datoru saraksts ar statusiem."""
    datori = Dators.query.all()
    return render_template('datoru_saraksts.html', datori=datori)


@app.route('/lietotaji')
def lietotaji():
    """Reģistrēto skolotāju saraksts."""
    skolotaji = Skolotajs.query.all()
    return render_template('lietotaji.html', skolotaji=skolotaji)


@app.route('/statistika')
def statistika():
    """Visu lietojumu vēsture."""
    lietojumi = Lietojums.query.all()
    return render_template('statistika.html', lietojumi=lietojumi)


@app.route('/panemt', methods=['POST'])
def panemt_datoru():
    """Reģistrē datora paņemšanu — maina statusu uz 'aizņemts'."""
    dators_id = int(request.form['dators_id'])
    skolotajs_id = int(request.form['skolotajs_id'])

    dators = Dators.query.get(dators_id)

    if dators.statuss == 'pieejams':
        dators.statuss = 'aizņemts'
        jauns_lietojums = Lietojums(dators_id=dators_id, skolotajs_id=skolotajs_id)
        db.session.add(jauns_lietojums)
        db.session.commit()
        flash('Dators veiksmīgi paņemts!', 'success')
    else:
        flash('Šis dators jau ir aizņemts!', 'error')

    return redirect(url_for('index'))


@app.route('/atgriezt/<int:datora_id>')
def atgriezt_datoru(datora_id):
    """Reģistrē datora atgriešanu — maina statusu uz 'pieejams'."""
    dators = Dators.query.get(datora_id)

    if dators.statuss == 'aizņemts':
        dators.statuss = 'pieejams'

        # Atrod aktīvo lietojumu un pieraksta beigu laiku
        aktivs_lietojums = Lietojums.query.filter_by(
            dators_id=datora_id,
            beigas=None
        ).first()

        if aktivs_lietojums:
            aktivs_lietojums.beigas = datetime.utcnow()

        db.session.commit()
        flash('Dators veiksmīgi atgriezts!', 'success')
    else:
        flash('Dators jau ir pieejams!', 'info')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # Inicializē datubāzi pirms lietotnes palaišanas
    with app.app_context():
        setup_db()
    app.run(debug=True)

