from dateutil import parser
import datetime, time
import unittest
import pandas as pd
import MissedRevenueHeatmapGenerator


#Use pandas to easily manage data and extract important information

MR = MissedRevenueHeatmapGenerator.MissedRevenueHeatmapGenerator()

# Methods in the MissedRevenueHeatmapGenerator class
#============================================================================================================================================

#calculate_business_hours(self, branch_dict):

#calculate_stock_level(self,sku, branch, journal, stock_level):

#calculate_danger_periods(self, sku, branch, danger_level, stock_level):

#calculate_average_rate_of_sale_per_hour(self,sku, branch, journal, business_hours, date_range):

#calculate_run_rate(self,sku, branch, journal, rate_of_sale_per_hour, business_hours_per_day):

#calculate_missed_revenue(self, sku, branch, journal, retail_price, danger_period):

#============================================================================================================================================

#All unittests were written under the following assumptions:
#   (1) testing functions for one product(sku) at one branch
#   (2) parsing of csv files are errorless
#   (3) constant rate of sale for any product at any branch
#   (4) business hours for a branch is 9am - 7pm (10 hours)

class TestMissedRevenueHeatmapGenerator(unittest.TestCase):

    def test_calculate_business_hours(self):
        #this will test the calculate_business_hours func
        #to ensure that a branch's business hours are calculated correctly
        #test parameters
        branch = 'Cape Town'
        #assume each branch is represented in a dict, with it's name and business hours
        #business hours [days, hours_per_day]
        Branch_info = {'name': branch,'business_hours':[7, 10]} 
        days, hours = Branch_info['business_hours']
        expected_business_hours = days * hours
        #method from MissedRevenueHeatmapGenerator
        calculated_business_hours = MR.calculate_business_hours(Branch_info)
        
        self.assertEqual(calculated_business_hours, expected_business_hours)


        
    
    def test_calculate_stock_level(self):
        #this will effectively test whether the calculate_stock_level func
        #calculates the stock level correctly
        #this function is called at the time of opening/closing or when a journal entry is made
        #===============
        #test parameters
        sku = 'FON6-TPD-WHT'
        branch = 'Cape Town'
        date ='2016-01-29T08:15:49.213+02:00'
        initial_stock_level = 500 #assume stock level
        #assume that NEW entries from wefix-sample-stock-journal.csv will be parsed into a dict named 'journal'
        journal = [{'Branch':branch, 'Date':date, 'Increment':-1,'Sku':sku,'Tag':'sale'},{'Branch':branch, 'Date':date, 'Increment':-1,'Sku':sku,'Tag':'sale'}]
        #use pandas to create a temporary csv file, for extracting data
        df = pd.DataFrame(journal, columns = ['Branch','Date','Increment','Sku','Tag'])
        #use pandas count() to count the number of sales
        sales = df['Tag'][df['Tag'] == 'sale'].count()
        expected_stock_level = initial_stock_level - sales
        #method from MissedRevenueHeatmapGenerator
        calculated_stock_level = MR.calculate_stock_level(sku, branch, journal, initial_stock_level)
        
        self.assertEqual(calculated_stock_level, expected_stock_level)

        


    def test_calculate_danger_periods(self):
        #we want to know when stock_level < danger_level
        #when stock_level < danger_level save the time
        #then when stock_level > danger_level close the window
        sku = 'FON6-TPD-WHT'
        branch = 'Cape Town'
        danger_level = 10
        initial_stock_level = 10
        stock_level = 0 #dummy stock level
        t1 = ''
        t2 = ''
        flag = False
        journal = [{'Branch':branch, 'Date':'2016-01-29T08:15:49.213+02:00', 'Increment':-1,'Sku':sku,'Tag':'sale'},{'Branch':branch, 'Date':'2016-01-29T10:15:49.213+02:00', 'Increment':+10,'Sku':sku,'Tag':'purchase'}]
        for entry in journal:
            effect_on_stock = entry['Increment']
            stock_level = initial_stock_level + effect_on_stock
            if stock_level < danger_level and flag == False:
                t1 = entry['Date']
                flag = True
            elif stock_level > danger_level and flag == True:
                t2 = entry['Date']
        expected_danger_period = (t1,t2)
        #method from MissedRevenueHeatmapGenerator
        calculated_danger_period = MR.calculate_danger_periods(sku, branch,danger_level, stock_level)
        
        self.assertEqual(calculated_danger_period, expected_danger_period)




    def test_calculate_average_rate_of_sale_per_day(self):
        sku = 'FON6-TPD-WHT'
        branch = 'Cape Town'
        business_hours_per_day = 10 #assume business hours 9am - 7pm
        date_range = ('2016-01-29T08:15:49.213+02:00', '2016-01-29T10:15:49.213+02:00') #date_range is a tuple containing two dates in string format
        sales = 0
        #assume that NEW entries from wefix-sample-stock-journal.csv will be parsed into a dict named 'journal'
        journal = [{'Branch':branch, 'Date':'2016-01-29T08:15:49.213+02:00', 'Increment':-6,'Sku':sku,'Tag':'sale'},{'Branch':branch, 'Date':'2016-01-29T10:15:49.213+02:00', 'Increment':-7,'Sku':sku,'Tag':'sale'}]
        #use pandas to create a temporary csv file, for extracting data
        for entry in journal:
            if (entry['Date'] >= date_range[0]) and (entry['Date'] <= date_range[1]) and entry['Tag'] == 'sale':
                sales -= entry['Increment']
        expected_sales_per_hour = sales/business_hours_per_day
        #method from MissedRevenueHeatmapGenerator
        calculated_average_rate_of_sale_per_hour = MR.calculate_average_rate_of_sale_per_day(sku, branch, journal, business_hours_per_day, date_range)
        
        self.assertEqual(calculated_average_rate_of_sale_per_hour, expected_sales_per_hour)




    def test_calculate_run_rate(self):
        #assume that the run rate is calculated to predict daily run rate
        sku = 'FON6-TPD-WHT'
        branch = 'Cape Town'
        #assume that NEW entries from wefix-sample-stock-journal.csv will be parsed into a dict named 'journal'
        journal = [{'Branch':branch, 'Date':'2016-01-29T08:15:49.213+02:00', 'Increment':-6,'Sku':sku,'Tag':'sale'},{'Branch':branch, 'Date':'2016-01-29T10:15:49.213+02:00', 'Increment':-7,'Sku':sku,'Tag':'sale'}]
        average_sales_per_hour = 1.3
        business_hours_per_day = 10
        expected_run_rate = average_sales_per_hour * business_hours_per_day
        #method from MissedRevenueHeatmapGenerator
        calculated_run_rate = MR.calculate_run_rate(sku, branch, journal, average_sales_per_hour, business_hours_per_day)
        
        self.assertEqual(calculated_run_rate, expected_run_rate)
        


        
    def test_calculate_missed_revenue(self):
        #test parameters
        sku = 'FON6-TPD-WHT'
        branch = 'Cape Town'
        business_hours_per_day = 10 #assume business hours 9am - 7pm
        average_rate_of_sales = 1.3 #estimated units sold per hour
        run_rate = 13
        retail_price = 699
        danger_period = ('2016-01-29T08:15:49.213+02:00', '2016-01-29T10:15:49.213+02:00')
        dt1 = parser.parse(danger_period[0])
        dt2 = parser.parse(danger_period[1])
        danger_time = (dt2 - dt1).total_seconds()/3600 # calculate total hours
        journal = [{'Branch':branch, 'Date':'2016-01-29T08:15:49.213+02:00', 'Increment':-1,'Sku':sku,'Tag':'sale'},{'Branch':branch, 'Date':'2016-01-29T15:15:49.213+02:00', 'Increment':10,'Sku':sku,'Tag':'purchase'}]
        #if we assume a constant rate of sales, then we can calculate missed revenue as:
        expected_missed_revenue = danger_time*average_rate_of_sales*retail_price
        #method from MissedRevenueHeatmapGenerator
        calculated_missed_revenue = MR.calculate_missed_revenue(sku, branch, journal, retail_price, danger_time)
        
        self.assertEqual(calculated_missed_revenue, expected_missed_revenue)





if __name__ == '__main__':
    unittest.main()


