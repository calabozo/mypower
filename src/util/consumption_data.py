from datetime import datetime

class ConsumptionData(object):
    def __init__(self,probe_id):
        self.probe_id = probe_id
        self.vrms = None
        self.irms = None
        self.power_aparent = None
        self.power_active = None
        self.power_reactive_ind = None
        self.power_reactive_cap = None
        self.frequency = None
        self.energy_active = None
        self.energy_reactive_ind = None
        self.energy_reactive_cap = None
        self.price = None

    def parse_xml(self,probe_label,exml):
        timestamp = int(exml.find('time').text)
        self.time = datetime.fromtimestamp(timestamp)
        self.vrms = float(exml.find('%s_vrms'%probe_label).text)
        self.irms = float(exml.find('%s_irms' % probe_label).text)
        self.power_aparent = float(exml.find('%s_p_aparent' % probe_label).text)
        self.power_active = float(exml.find('%s_p_activa' % probe_label).text)
        self.power_reactive_ind = float(exml.find('%s_p_reactiva_ind' % probe_label).text)
        self.power_reactive_cap = float(exml.find('%s_p_reactiva_cap' % probe_label).text)
        self.frequency = float(exml.find('%s_frecuencia' % probe_label).text)
        self.energy = None
        self.energy_active = float(exml.find('%s_energia_activa' % probe_label).text)
        self.energy_reactive_ind = float(exml.find('%s_energia_reactiva_ind' % probe_label).text)
        self.energy_reactive_cap = float(exml.find('%s_energia_reactiva_cap' % probe_label).text)
        self.price = None

    def parse_db(self,row):
        self.vrms = float(row['vrms'])
        self.irms = float(row['irms'])
        self.power_aparent = float(row['power_aparent'])
        self.power_active = float(row['power_active'])
        self.power_reactive_ind = float(row['power_reactive_ind'])
        self.power_reactive_cap = float(row['power_reactive_cap'])
        self.frequency = float(row['frequency'])
        self.energy_active = float(row['energy_active'])
        self.energy_reactive_ind = float(row['energy_reactive_ind'])
        self.energy_reactive_cap = float(row['energy_reactive_cap'])
        self.energy = float(row['energy'])
        self.price = float(row['price'])

    def set_energy(self,energy,time):
        self.time = time
        self.energy = energy

    def calc_energy(self,prev_consumption_data):
        if (prev_consumption_data is None or prev_consumption_data.energy_active is None):
            self.energy = 0
        else:
            self.energy = self.energy_active - prev_consumption_data.energy_active

    def set_tariff(self,tariff):
        self.price=tariff.get_price(self.time)*self.energy/1000


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
        out += '  energy: %s\n' % self.energy
        out += '  energy_active:%s\n' % self.energy_active
        out += '  energy_reactive_ind:%s\n' % self.energy_reactive_ind
        out += '  energy_reactive_cap:%s\n' % self.energy_reactive_cap
        out += '  price:%s\n' % self.price
        return out

class Tariff(object):
    def __init__(self, tariff):
        self.valley = float(tariff['valley'])
        self.peak = float(tariff['peak'])

    def get_price(self,time):
        if time.hour >= 12 and time.hour < 22:
            return self.peak
        else:
            return self.valley

class Taxes(object):
    class Tax(object):
        def __init__(self,tax):
            self.name = tax['name']
            self.value = float(tax['value'])
            self.relabs = bool(tax['relabs'])


    def __init__(self,db_taxes):
        self.taxes = []
        for tax in db_taxes:
            self.taxes.append(Taxes.Tax(tax))

    def calculate_taxes(self,amount):
        final_tax= 0
        for tax in self.taxes:
            if (tax.relabs):
                final_tax += tax.value/100.0*amount
            else:
                final_tax += tax.value
        return final_tax

class MonthlyConsumption(object):
    def __init__(self, row):
        self.energy = float(row['energy'])
        self.price  = float(row['price'])
        self.month  = row['month']

    def __str__(self):
        out = 'Energy: %s, Price: %s, Month: %s'%(
                str(self.energy),str(self.price),str(self.month))
        return out




