#!/usr/bin/env python2


import requests
import logging
from datetime import datetime
import argparse
import xml.etree.ElementTree
from sqlalchemy import create_engine


class ConsumptionData(object):

    def __init__(self,probe_id,probe_label,exml):
        self.probe_id = probe_id
        timestamp = int(exml.find('time').text)
        self.time = datetime.fromtimestamp(timestamp)
        self.vrms = float(exml.find('%s_vrms'%probe_label).text)
        self.irms = float(exml.find('%s_irms' % probe_label).text)
        self.power_aparent = float(exml.find('%s_p_aparent' % probe_label).text)
        self.power_active = float(exml.find('%s_p_activa' % probe_label).text)
        self.power_reactive_ind = float(exml.find('%s_p_reactiva_ind' % probe_label).text)
        self.power_reactive_cap = float(exml.find('%s_p_reactiva_cap' % probe_label).text)
        self.frequency = float(exml.find('%s_frecuencia' % probe_label).text)
        self.energy_active = float(exml.find('%s_energia_activa' % probe_label).text)
        self.energy_active_ind = float(exml.find('%s_energia_reactiva_ind' % probe_label).text)
        self.energy_active_cap = float(exml.find('%s_energia_reactiva_cap' % probe_label).text)
        self.price = None


    def __str__(self):
        out = 'probe_id:%d\n'%self.probe_id
        out += '  time:%s\n' % self.time
        out += '  vrms:%s\n' % self.vrms
        out += '  irms:%s\n' % self.irms
        out += '  power_aparent:%s\n' % self.power_aparent
        out += '  power_active:%s\n' % self.power_active
        out += '  power_reactive_ind:%s\n' % self.power_reactive_ind
        out += '  power_reactive_cap:%s\n' % self.power_reactive_cap
        out += '  frequency:%s\n' % self.frequency
        out += '  energy_active:%s\n' % self.energy_active
        out += '  energy_active_ind:%s\n' % self.energy_active_ind
        out += '  energy_active_cap:%s\n' % self.energy_active_cap
        out += '  price:%s\n' % self.price


        return out


class DataBaseUtil(object):

    def __init__(self):
        pass

    def get_probes(self):
        pass

    def get_tariff(self):
        pass

    def save_data(self,data_row):
        pass

    def save_tarif(self,data_row):
        pass

def launch_query(url = "http://192.168.0.159/en/status.xml"):
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

    e = xml.etree.ElementTree.fromstring(r.text)
    return e



if __name__=="__main__":

    parser = argparse.ArgumentParser(
        description='Downloads data from Mirubox.',
        epilog='''It stores the data in the table data and calculates its price.''')
    parser.add_argument('--log' ,metavar='LEVEL', help='Set log level. ERROR, WARNING, INFO, DEBUG', default='DEBUG')
    parser.add_argument('--logFile' ,metavar='LOG_FILE', help='Saves the log info in a file.',default=None)

    args = parser.parse_args()

    loglevel =args.log
    log_file =args.logFile

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)


    logging.basicConfig(filename=log_file ,format='%(asctime)s %(levelname)s:\t%(message)s' ,level=numeric_level)
    exml = launch_query()
    cmpdata = ConsumptionData(1,'fase1',exml)
    print(cmpdata)