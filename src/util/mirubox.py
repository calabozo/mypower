import logging
import xml.etree.ElementTree
from db.dao import Dao
from util.consumption_data import ConsumptionData
import requests
import csv
from datetime import datetime


def launch_query_and_save_in_db(host):
    url = "http://{host}/en/status.xml".format(host=host)
    logging.debug("Sending query: {url}".format(url=url))
    try:
        r = requests.get(url)
    except requests.exceptions.Timeout:
        logging.error("Request timeout" )
        return None
    except Exception as err:
        logging.error("%s" % (str(err)))
        return None

    sc = r.status_code

    if sc != 200:
        logging.error("The request returned status code {status}".format(status=sc))

    exml = xml.etree.ElementTree.fromstring(r.text)

    db = Dao(user='userdb', password='passwdb', host='db')

    db.connect()

    probes = db.get_real_probes()
    tariff = db.get_tariff(1)

    for probe in probes:
        last_data = db.get_last_sample_from_probe(probe['id'])

        cmpdata = ConsumptionData(probe['id'])
        cmpdata.parse_xml(probe['label'], exml)
        cmpdata.calc_energy(last_data)
        cmpdata.set_tariff(tariff)
        if cmpdata.energy>0:
            db.save_data(cmpdata)

    db.disconnect()

def read_data_and_save_in_db(file_name):
    db = Dao(user='userdb', password='passwdb', host='db')
    db.connect()
    def save_probe_data(probe_id,energy,time,tariff ):
        if probe_id is None:
            return
        cmpdata = ConsumptionData(probe_id)
        cmpdata.set_energy(energy,time)
        cmpdata.set_tariff(tariff)
        db.save_data(cmpdata)

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0

        probe_id1 = db.get_probe_from_label('fase1')['id']
        probe_id2 = db.get_probe_from_label('fase2')['id']
        probe_id3 = db.get_probe_from_label('fase3')['id']

        tariff = db.get_tariff(1)

        for row in csv_reader:
            if line_count > 0:
                energy_fase1 = float(row[0])
                energy_fase2 = float(row[1])
                energy_fase3 = float(row[2])
                time = datetime.strptime(row[3],'%d/%m/%Y %H:%M:%S')

                save_probe_data(probe_id1, energy_fase1,time, tariff )
                save_probe_data(probe_id2, energy_fase2, time, tariff )
                save_probe_data(probe_id3, energy_fase3, time, tariff )

            line_count += 1
    
    db.disconnect()
