import unittest
import DataExtractor
import datetime


class TestDataExtractorTests(unittest.TestCase):
#============================================================================================================================================
    def test_calculate_missed_revenue_at_branch_for_sku_between(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'},{'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'}) #requires more entries for date_range
        date_range = (datetime.date(2016,1,29), datetime.date(2016,1,29)) #tuple (start, end)
        sku = d._extract_sku(journal)
        branch = d._extract_branch(journal)
        calculated_missed_revenue = d.calculate_missed_revenue_at_branch_for_sku_between(sku, branch, date_range, journal)
        #TODO: calculate actual missed revenue
        #actual_missed_revenue = missed_qty * retail_price
        actual_missed_revenue = 15000
        self.assertEqual(calculated_missed_revenue, actual_missed_revenue)

    def test_calculate_missed_revenue_with_no_data_for_date_range(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'},{'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'}) #requires more entries for date_range
        date_range = (datetime.date(2016,1,30), datetime.date(2016,1,30)) #tuple (start, end)
        sku = d._extract_sku(journal)
        branch = d._extract_branch(journal)
        calculated_missed_revenue = d.calculate_missed_revenue_at_branch_for_sku_between(sku, branch, date_range, journal)
        self.assertEqual(calculated_missed_revenue, 500)
        

    def test_calculate_rate_of_sale(self):
        #this test covers cases where the date_range has no accompanying data
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        date_range = (datetime.date(2016,1,29), datetime.date(2016,1,29)) #tuple (start, end)
        sku = d._extract_sku(journal)
        branch = d._extract_branch(journal)
        rate_of_sale = d.calculate_rate_of_sale(sku, branch, date_range, journal)
        #TODO: calculate actual rate of sales
        temp_rate_of_sale = 5 
        self.assertEqual(rate_of_sale, 5)
        

    def test_calculate_stock_level(self):
        #Assuming that stock level is known, thus dummy_stock_level == stock_level from extracted with class method
        dummy_stock_level = 1000 #change
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        sku = d._extract_sku(journal)
        timestamp = d._extract_date(journal)
        branch = d._extract_branch(journal)
        stock_level = d.calculate_stock_level(sku, timestamp, branch, journal)
        dummy_stock_level = dummy_stock_level + (-1)#d._extract_increment(journal)
        self.assertEqual(stock_level, 999)

    def test_calculate_rate_of_sales_over_time(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        date_range = (datetime.date(2016,1,29), datetime.date(2016,1,29)) #tuple (start, end)
        #TODO: calculate rate over time for this specific instance to compare to class method
        rate_of_sale_over_time = d.calculate_rate_of_sales_over_time(journal, date_range, lambda: d.aggregation_fn())
        self.assertEqual(rate_of_sale_over_time, 1)

    #def test_aggregation_fn(self):
        #average = calculate actual average
        #TODO: test actual aggregation function's accuracy
        #self.assertEqual(average_fn(), average)


#Test utility functions
#============================================================================================================================================
    def test_extract_date(self):
        #check if _extract_date functions as intended
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        date = d._extract_date(journal)
        self.assertEqual(date, '2016-01-29')

    def test_extract_date_with_malformed_date(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2mjh6-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        #we expect to see a typeError when the date format is incorrect
        with self.assertRaises(TypeError):
             date = d._extract_date(journal)

    def test_extract_date_with_invalid_date(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-299', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        #we expect to see a ValueError when the date format is malformed
        with self.assertRaises(ValueError):
             date = d._extract_date(journal)     

    def test_extract_date_with_missing_date(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        #we expect to see a KeyError when the date is missing
        with self.assertRaises(KeyError):
             date = d._extract_date(journal)


    def test_extract_branch(self):
        #check if _extract_branch functions as intended
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        branch = d._extract_branch(journal)
        self.assertEqual(branch, 'Fourways')

    def test_extract_branch_with_invalid_branch(self):
        d = DataExtractor.DataExtractor()
        journal = ({'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        #check whether branch is in a list of valid branches
        branch = d._extract_branch(journal)

    def test_extract_branch_with_missing_branch(self):
        d = DataExtractor.DataExtractor()
        journal = ({'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        #we expect to see a KeyError when the branch is missing
        with self.assertRaises(KeyError):
             branch = d._extract_branch(journal)


    def test_extract_increment(self):
        #check if _extract_increment functions as intended
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        inc = d._extract_increment(journal)
        self.assertEqual(inc, -1)

    def test_extract_increment_with_invalid_increment(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':'a','sku':'FON6-TPD-WHT','tag':'sale'})
        #we expect to see a TypeError when the increment is not an integer
        with self.assertRaises(TypeError):
             inc = d._extract_increment(journal)


    def test_extract_sku(self):
        #check if _extract_sku functions as intended
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        sku = d._extract_sku(journal)
        self.assertEqual(sku, 'FON6-TPD-WHT')

    def test_extract_sku_with_invalid_sku(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'Invalid_sku','tag':'sale'})
        sku = d._extract_sku(journal)
        #check whether sku is in a list of valid sku's
        self.assertEqual(sku, False)

    def test_extract_sku_with_sku_missing(self):
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'tag':'sale'})
        #we expect to see a KeyError when the sku is missing
        with self.assertRaises(KeyError):
            sku = d._extract_sku(journal)


    def test_extract_tag(self):
        #check if _extract_tag functions as intended
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':'sale'})
        tag = d._extract_tag(journal)
        self.assertEqual(tag, 'sale')

    def test_extract_tag_with_invalid_tag(self):
        #check if tag is in a list of possible tags
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':-1,'sku':'FON6-TPD-WHT','tag':33})
        tag = d._extract_tag(journal)
        self.assertEqual(tag, False)
        
    def test_increment(self):
        #check if tag is coherent with increment
        d = DataExtractor.DataExtractor()
        journal = ({'branch':'Fourways', 'date':'2016-01-29', 'increment':1,'sku':'FON6-TPD-WHT','tag':'sale'})
        tag = d._extract_tag(journal)
        self.assertEqual(tag, False)

if __name__ == '__main__':
    unittest.main()
