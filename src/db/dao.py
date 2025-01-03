import psycopg2
import psycopg2.extras
import logging
from util.consumption_data import ConsumptionData, Tariff, MonthlyConsumption, Taxes


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

    def disconnect(self):
        self.conn.close()

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
        cur.execute("SELECT * from tariff WHERE id=%s AND from_date<=current_date AND to_date>=current_date;",(tariff_id,))
        tariff = cur.fetchone()
        cur.close()
        return Tariff(tariff)


    def get_taxes(self):
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * from taxes;")
        taxes = cur.fetchall()
        cur.close()
        return Taxes(taxes)

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
        cur.execute(sql, (probe_id,))
        row=cur.fetchone()
        if row is None or row['vrms'] is None:
            return None
        cmpdata = ConsumptionData(row['probe_id'])
        cmpdata.parse_db(row)
        cur.close()
        return cmpdata

    def get_monthly_consumption(self,probe_id,mode='all'):
        #TODO: Summer and winter daylight savings
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        base_sql = "select sum(energy) as energy,sum(price) as price,to_char(time,'YYYY-MM') as month from data where probe_id=%s and time>='2024-08-04 10:30' and energy>0 and energy<1000 {} group by to_char(time, 'YYYY-MM') order by month desc;"

        if mode == 'all':
            sql = base_sql.format("")
        elif mode == 'peak':
            sql = base_sql.format("and extract(isodow from time)<6 and (extract(hour from time)>=10 AND extract(hour from time)<14 OR  extract(hour from time)>=18 AND extract(hour from time)<22) ")
        elif mode == 'flat':
            sql = base_sql.format("and extract(isodow from time)<6 and (extract(hour from time)>=8 AND extract(hour from time)<10 OR  extract(hour from time)>=14 AND extract(hour from time)<18 OR  extract(hour from time)>=22 AND extract(hour from time)<24) ")
        elif mode == 'valley':
            sql = base_sql.format("and (extract(isodow from time)>=6 OR extract(hour from time)<8)")

        cur.execute(sql, (probe_id,))
        rows=cur.fetchall()
        monthly_consumptions = []
        for row in rows:
            monthly_consumptions.append(MonthlyConsumption(row))
        cur.close()
        return monthly_consumptions



