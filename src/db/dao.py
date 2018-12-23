import psycopg2
import psycopg2.extras
import logging
from util.consumption_data import ConsumptionData, Tariff


class Dao(object):
    def __init__(self,user,password,host,port=5432,database='consumption'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database


    def connect(self):
        self.conn = psycopg2.connect(user=self.user, password=self.password, host=self.host,
                                     port=self.port, dbname=self.database)

        pass

    def get_real_probes(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * from probes WHERE realvirtual=TRUE;")
        probes = cur.fetchall()
        cur.close()
        return probes

    def get_probe_from_label(self,label):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * from probes WHERE label=%s;",(label,))
        probes = cur.fetchone()
        cur.close()
        if probes is None:
            probes={'id':None}
        return probes

    def get_tariff(self,tariff_id):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * from tariff WHERE id=%s;",(tariff_id,))
        tariff = cur.fetchone()
        cur.close()
        return Tariff(tariff)

    def save_data(self,consumption_data):
        sql = "INSERT INTO data (probe_id, time, vrms,irms, power_aparent, power_active, power_reactive_ind, " \
              "power_reactive_cap, frequency, energy, energy_active, energy_reactive_ind, energy_reactive_cap, price) " \
              "VALUES (%s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cur = self.conn.cursor()
        cur.execute(sql,(consumption_data.probe_id,
                         consumption_data.time, consumption_data.vrms, consumption_data.irms,
                         consumption_data.power_aparent,consumption_data.power_active,
                         consumption_data.power_reactive_ind, consumption_data.power_reactive_cap,
                         consumption_data.frequency, consumption_data.energy,
                         consumption_data.energy_active, consumption_data.energy_reactive_ind,
                         consumption_data.energy_reactive_cap, consumption_data.price))
        logging.debug("Inserted entry for probe_id:%d",consumption_data.probe_id)
        self.conn.commit()
        cur.close()

    def get_last_sample_from_probe(self,probe_id):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT * from data WHERE probe_id=%s ORDER BY time DESC LIMIT 1;"
        row=cur.fetchone()
        cmpdata = ConsumptionData(row['id'])
        cmpdata.parse_db(row)
        cur.close()
        return cmpdata


    def update_price(self,data_row):

        pass
