from unittest import TestCase
from datetime import datetime, timedelta


from util.consumption_data import ConsumptionData, Tariff
from db.dao import Dao

class TestConsumption(TestCase):

    def test_tariff(self):
        peak_price = 10
        valley_price = 2


        tariff = Tariff({'valley':valley_price,'peak':peak_price})

        mydate = datetime(2018,01,01)

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
