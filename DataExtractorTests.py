import unittest
import DataExtractor
import datetime


class TestDataExtractorFunctions(unittest.TestCase):

    def test_calculate_missed_revenue_at_branch_for_sku_between(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        date_range = (datetime.date(2014,3,1), datetime.date(2014,3,1))
        calculated_missed_revenue = d.calculate_missed_revenue_at_branch_for_sku_between("ABC", "Cape Town", date_range, journal)
        self.assertEqual(calculated_missed_revenue, None)
        #==================================================

        #TODO: negative tests
        #malformed input parameter
        #sku does not exist
        #No data for date_range
        #Tag does not match increment
        

    def test_calculate_rate_of_sale(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        date_range = (datetime.date(2014,3,1), datetime.date(2014,3,1))
        rate_of_sale = d.calculate_rate_of_sale(journal, date_range, aggregation_fn)
        
        #==================================================

        #TODO: negative tests
        #Malformed input parameter
        #aggregation_fn incorrect
        #No data for date_range

    def test_calculate_stock_level(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        stock_level = d.calculate_stock_level()
        #==================================================

        #TODO: negative tests
        #Malformed input parameter
        #Invalid date
        #Date does not exist

    def test_calculate_rate_of_sales_over_time(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        #==================================================
        
        #TODO: negative tests
        #Malformed date
        #Invalid date
        #Date does not exist


#Test utility functions


    def test_extract_date(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        date = d._extract_date(journal)
        self.assertEqual(date, '2016-01-29')
        #==================================================
        
        #TODO: negative tests
        #Malformed date
        #Invalid date
        #Date does not exist

    
    def test_extract_branch(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        branch = d._extract_branch(journal)
        self.assertEqual(branch, 'Fourways')
        #==================================================

        #TODO: negative tests
        #Invalid branch name
        #Branch name does not exist

    def test_extract_increment(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        inc = d._extract_increment(journal)
        self.assertEqual(inc, -1)
        #==================================================

        #TODO: negative tests
        #Malformed increment
        #Invalid increment

    def test_extract_sku(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        sku = d._extract_sku(journal)
        self.assertEqual(sku, 'FON6-TPD-WHT')
        #==================================================

        #TODO: negative tests
        #Invalid sku
        #sku does not exist

    def test_extract_tag(self):
        #==================================================
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        tag = d._extract_tag(journal)
        self.assertEqual(tag, 'sale')
        #==================================================

        #TODO: negative tests
        #Invalid tag

if __name__ == '__main__':
    unittest.main()
