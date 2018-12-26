from flask import Flask
from db.dao import Dao

app = Flask(__name__)


@app.route('/')
def index():
    dao = Dao(user='userdb', password='passwdb', host='127.0.0.1')
    dao.connect()
    tariff = dao.get_tariff(1)
    dao.disconnect()

    html_title='<h1>Consumo</h1>'
    html_tariff='Tarifa valle (22h-12h):%.6f    Tarifa pico(12h-22h):%.6f'%(tariff.valley,tariff.peak)
    #html_tariff='xxx'

    return html_title+'<br/>'+html_tariff
