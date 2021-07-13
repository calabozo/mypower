from unittest import TestCase
from datetime import datetime, timedelta


from util.consumption_data import ConsumptionData, Tariff, Taxes
from db.dao import Dao

class TestConsumption(TestCase):

    def test_tariff(self):
        peak_price = 10
        valley_price = 2


        tariff = Tariff({'valley':valley_price,'peak':peak_price})

        mydate = datetime(2018,1,1)

        for h in xrange(0,12):
            price=tariff.get_price(mydate+timedelta(hours=h))
            self.assertEqual(price,valley_price)

        for h in xrange(12,22):
            price=tariff.get_price(mydate+timedelta(hours=h))
            self.assertEqual(price,peak_price)

        for h in xrange(22,25):
            price=tariff.get_price(mydate+timedelta(hours=h))
            self.assertEqual(price,valley_price)

    def test_consumption_data_db(self):
        vrms = 230
        energy_active= 1000
        energy = 10
        price = 30
        row={'vrms':vrms,'energy_active':energy_active,'energy':energy,'price':price,
             'irms':1,'power_aparent':1,'power_active':1,'power_reactive_ind':1,'power_reactive_cap':1,
             'frequency':1,'energy_reactive_ind':1,'energy_reactive_cap':1}
        cmp =ConsumptionData(100)
        cmp.parse_db(row)

        self.assertEqual(cmp.vrms,vrms)
        self.assertEqual(cmp.energy_active, energy_active)
        self.assertEqual(cmp.energy, energy)
        self.assertEqual(cmp.price, price)

    def test_taxes(self):
        tax_1_name = 'electricidad'
        tax_1_value = 5
        tax_1_relabs = True

        tax_2_name = 'IVA'
        tax_2_value = 20
        tax_2_relabs = True

        tax_3_name = 'fijo'
        tax_3_value = 5
        tax_3_relabs = False

        db_taxes = [{'name':tax_1_name,'value':tax_1_value,'relabs':tax_1_relabs},
                    {'name': tax_2_name, 'value': tax_2_value, 'relabs': tax_2_relabs},
                    {'name': tax_3_name, 'value': tax_3_value, 'relabs': tax_3_relabs}]

        taxes = Taxes(db_taxes)
        amount = 100.0
        self.assertEqual(taxes.calculate_taxes(amount),float(tax_1_value+tax_2_value)/100.0*amount+tax_3_value)
        amount = 3.45
        self.assertEqual(taxes.calculate_taxes(amount), float(tax_1_value + tax_2_value) / 100.0 * amount + tax_3_value)