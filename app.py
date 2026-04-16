from flask import Flask, render_template, redirect, url_for, request, flash
from models.models import db, Dators, Skolotajs, Lietojums
from config import Config
from utils.external_api import get_weather_info
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request
def setup_db():
    db.create_all()
    # Ja datubāze ir tukša, pievieno testa ierakstus
    if not Dators.query.first():
        d1 = Dators(nosaukums='Chromebook 1')
        d2 = Dators(nosaukums='Chromebook 2')
        s1 = Skolotajs(vards='Anna', uzvards='Ozola', epasts='anna@skola.lv')
        s2 = Skolotajs(vards='Jānis', uzvards='Kalns', epasts='janis@skola.lv')
        db.session.add_all([d1, d2, s1, s2])
        db.session.commit()

@app.route('/')
def index():
    datori = Dators.query.all()
    laikapst = get_weather_info()
    return render_template('index.html', datori=datori, laikapst=laikapst)

@app.route('/datori')
def datoru_saraksts():
    datori = Dators.query.all()
    return render_template('datoru_saraksts.html', datori=datori)

@app.route('/lietotaji')
def lietotaji():
    skolotaji = Skolotajs.query.all()
    return render_template('lietotaji.html', skolotaji=skolotaji)

@app.route('/statistika')
def statistika():
    lietojumi = Lietojums.query.all()
    return render_template('statistika.html', lietojumi=lietojumi)

@app.route('/panemt', methods=['POST'])
def panemt_datoru():
    dators_id = int(request.form['dators_id'])
    skolotajs_id = int(request.form['skolotajs_id'])
    dators = Dators.query.get(dators_id)
    if dators.statuss == "pieejams":
        dators.statuss = "aizņemts"
        db.session.add(Lietojums(dators_id=dators_id, skolotajs_id=skolotajs_id))
        db.session.commit()
        flash("Dators veiksmīgi paņemts!", "success")
    else:
        flash("Šis dators jau ir aizņemts!", "error")
    return redirect(url_for('index'))

@app.route('/atgriezt/<int:datora_id>')
def atgriezt_datoru(datora_id):
    dators = Dators.query.get(datora_id)
    if dators.statuss == "aizņemts":
        dators.statuss = "pieejams"
        lietojums = Lietojums.query.filter_by(dators_id=datora_id, beigas=None).first()
        if lietojums:
            lietojums.beigas = datetime.utcnow()
        db.session.commit()
        flash("Dators veiksmīgi atgriezts!", "success")
    else:
        flash("Dators jau ir pieejams!", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
