import unittest
import datetime
import pandas as pd

# Methods in the MissedRevenueHeatmapGenerator class
#============================================================================================================================================

#calculate_run_rate(sku, branch, journal, date_range):

#calculate_missed_revenue(sku, branch, journal, business_hours, retail_price, stock_level):

#calculate_rate_of_sale(sku, branch, journal, business_hours):

#calculate_average_rate_of_sale(sku, branch, journal, business_hours, date_range):

#aggregate_sales(sku, branch, journal, date_range):

#calculate_stock_level(sku, branch, journal, stock_level):

#============================================================================================================================================

class TestMissedRevenueHeatmapGenerator(unittest.TestCase):
    
    def test_calculate_run_rate():
        pass
    def test_calculate_missed_revenue():
        pass
    def test_calculate_rate_of_sale():
        pass
    def test_calculate_average_rate_of_sale():
        pass
    def test_rate_of_sale_aggregator():
        pass
    def test_calculate_stock_level():
        #this will effectively test if the calculate_stock_level func
        #calculates the stock level correctly with each stock level
        sku = 'FON6-TPD-WHT'
        branch = 'Cape Town'
        timestamp ='2016-01-01'
        stock_level = 500 #test stock level
        journal = {'branch':branch, 'date':timestamp, 'increment':-1,'sku':sku,'tag':'sale'}
        calculated_stock_level = calculate_stock_level(sku, branch, journal, stock_level)
        self.assertEqual(calculated_stock_level, 499)
        

    


if __name__ == '__main__':
    unittest.main()
