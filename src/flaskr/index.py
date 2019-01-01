from flask import Flask, render_template
from db.dao import Dao

app = Flask(__name__)


@app.route('/')
def index():
    dao = Dao(user='userdb', password='passwdb', host='db')
    dao.connect()
    tariff = dao.get_tariff(1)

    taxes = dao.get_taxes()


    db_energy_total  = dao.get_monthly_consumption(2)
    db_energy_peak   = dao.get_monthly_consumption(2, mode = 'peak')
    db_energy_valley = dao.get_monthly_consumption(2, mode = 'valley')
    dao.disconnect()

    months = []
    energy_total = []
    price_total = []
    for e in db_energy_total:
        months.append(str(e.month))
        energy_total.append( str(e.energy/1e3))
        price_total.append( str(round((taxes.calculate_taxes(e.price)+e.price),2)))

    energy_peak = []
    for e in db_energy_peak:
        energy_peak.append(str(e.energy/1e3))

    energy_valley = []
    for e in db_energy_valley:
        energy_valley.append(str(e.energy/1e3))


    consumption = {'date':months,
                   'energy_total':energy_total,
                   'price_total': price_total,
                   'energy_peak': energy_peak,
                   'energy_valley':energy_valley}

    return render_template('index.html', tariff=tariff, consumption=consumption, taxes = taxes.taxes)
