from flask import Flask
from db.dao import Dao

app = Flask(__name__)


@app.route('/')
def index():
    dao = Dao(user='userdb', password='passwdb', host='127.0.0.1')
    dao.connect()
    tariff = dao.get_tariff(1)

    energy_total  = dao.get_monthly_consumption(2)
    energy_peak   = dao.get_monthly_consumption(2, mode = 'peak')
    energy_valley = dao.get_monthly_consumption(2, mode = 'valley')
    dao.disconnect()

    html_title='<h1>Consumo</h1>'
    html_tr1='<tr><td>Tarifa valle (22h-12h):</td><td>%.6f </td></tr>'%(tariff.valley)
    html_tr2='<tr><td>Tarifa pico  (12h-22h):</td><td>%.6f </td></tr>'%(tariff.peak)
    html_tariff='<table>%s%s</table>'%(html_tr1,html_tr2)

    html_date = ''
    html_energy_total = ''
    html_price_total = ''
    for e in energy_total:
        html_date += '<td>' + str(e.month) + '</td>'
        html_energy_total += '<td>' + str(e.energy/1e3) + '</td>'
        html_price_total += '<td>' + str(e.price) + '</td>'

    html_energy_peak = ''
    for e in energy_peak:
        html_energy_peak += '<td>' + str(e.energy/1e3) + '</td>'

    html_energy_valley = ''
    for e in energy_valley:
        html_energy_valley += '<td>' + str(e.energy/1e3) + '</td>'



    html_consumo = '<table>' + \
            '<tr><td> Fecha </td>' + html_date + '</tr>' + \
            '<tr><td>Consumo horario valle</td>' + html_energy_valley + '</tr>'+\
            '<tr><td>Consumo horario pico</td>' + html_energy_peak + '</tr>'+\
            '<tr><td>Consumo total kwh</td>' + html_energy_total + '</tr>' + \
            '<tr><td>Consumo precio</td>' + html_price_total + '</tr>' + \
            '</table>'

    return html_title+'<br/>'+html_tariff+'<br/>'+html_consumo
