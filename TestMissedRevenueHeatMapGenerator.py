import datetime, time
import unittest
import MissedRevenueHeatmapGenerator


# Methods in the MissedRevenueHeatmapGenerator class
#============================================================================================================================================

#calculate_stock_level(self,sku, branch, journal, stock_level):
    #return the stock levels of certain sku at a branch

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
#============================================================================================================================================
    sku = 'FON6-TPD-WHT'
    branch = 'Cape Town'
    #use cape town branch business hours
    #what about public holidays?
    #closed on sunday
    normal_business_hours = ['9am', '5pm']
    weekend_business_hours = ['9am', '1pm']
    
    business_hours = {'monday': normal_business_hours,
                      'tuesday': normal_business_hours,
                      'wednesday': normal_business_hours,
                      'thursday': normal_business_hours,
                      'saturday': weekend_business_hours}
    
    time_open = datetime.datetime(2017,1,3,9)
    time_close = datetime.datetime(2017,1,3,17)

    sale_1 = time_open + datetime.timedelta(hours=1)
    sale_2 = time_open + datetime.timedelta(hours=5)
    purchase_1 = time_open + datetime.timedelta(hours=2)
    purchase_2 = time_open + datetime.timedelta(hours=7)
#============================================================================================================================================
    def test_calculate_hours_a_branch_is_open(self):
        
        day_of_the_week = 'monday'
        #extract information from business_hours dict
        #what about public holidays
        #what about sundays?
        expected_hours_open = 8
        calculated_hours_open = calculate_hours_a_branch_is_open(branch, day_of_the_week, business_hours)
        self.assertEqual(calculated_stock_level, expected_stock_level)
    
    def test_calculate_stock_level_for_sku_at_specific_branch(self):
        #is increment the correct word for stock influencer
        #need sales and purchases to change stock level
        #assume stock level is:
        initial_stock_level = 500
        
        journal = [{'Branch':branch, 'Date':sale_1, 'Increment':-1,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':purchase_1, 'Increment':3,'Sku':sku,'Tag':'purchase'},
                   {'Branch':branch, 'Date':sale_2, 'Increment':-2,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':purchase_2, 'Increment':5,'Sku':sku,'Tag':'purchase'}]

        #500 - 1 + 3 - 2 + 5 
        expected_stock_level = 505
        calculated_stock_level = calculate_stock_level(sku, branch, journal, initial_stock_level)
        
        self.assertEqual(calculated_stock_level, expected_stock_level)

        


    def test_calculate_low_stock_level_periods(self):
        #calculate the periods in time for which stock level was below the danger level (zero stock)
        #assume danger level is 0
        stock_level = 0
        journal = [{'Branch':branch, 'Date':time_open, 'Increment':10,'Sku':sku,'Tag':'purchase'},
                   {'Branch':branch, 'Date':sale_1, 'Increment':-10,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':purchase_1, 'Increment':2,'Sku':sku,'Tag':'purchase'},
                   {'Branch':branch, 'Date':sale_2, 'Increment':-2,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':purchase_2, 'Increment':20,'Sku':sku,'Tag':'purchase'}]
        #can stock go below zero?
        #there are two periods during which stock is 0
        #period = (date_time_from, date_time_to)
        period_1 = (sale_1, purchase_1)
        period_2 = (sale_2, purchase_2)
        #are these periods during business hours??
        #what happens if it is outside business hours
        #return a tuple with time periods when stock was low (zero?)
        calculated_danger_period = calculate_danger_periods(sku, branch, journal, danger_level=0)
        self.assertEqual(calculated_danger_period, (period_1, period_2))




    def test_calculate_average_rate_of_sale_per_hour(self):
        #do we want to calculate ROS for one day only? longer periods?
        #reuse calculate_hours_a_branch_is_open function - calculate hours open during a specific day
        #3 Jan 2017 was a Tuesday
        hours_open = calculate_hours_a_branch_is_open(branch, 'tuesday', business_hours)
        
        journal = [{'Branch':branch, 'Date':sale_1, 'Increment':-6,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':purchase_1, 'Increment':2,'Sku':sku,'Tag':'purchase'},
                   {'Branch':branch, 'Date':sale_2, 'Increment':-7,'Sku':sku,'Tag':'sale'}]
        
        #increment of sales is negative - is this correct?
        #sales = 6 + 7
        sales = 13
        expected_average_rate_of_sale_per_hour = sales / hours_open
        calculated_average_rate_of_sale_per_hour = calculate_average_rate_of_sale_per_hour(sku, branch, journal, business_hours_per_day)
        self.assertEqual(calculated_average_rate_of_sale_per_hour, expected_sales_per_hour)




    def test_calculate_weekly_run_rate(self):
        #assume that the run rate is calculated to predict weekly run rate
        #how can we reuse to calculate monthly/quaterly/yearly run rate
        #TODO: figure out what this is supposed to do, how it will be used
        journal = [{'Branch':branch, 'Date':sale_1, 'Increment':-6,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':sale_2, 'Increment':-10,'Sku':sku,'Tag':'sale'}]
        
        hours_open = calculate_hours_a_branch_is_open(branch, 'tuesday', business_hours)
        average_sales_per_hour = 2
        days_open = 6
        
        expected_run_rate = average_sales_per_hour * hours_open * days_open
        calculated_run_rate = calculate_run_rate(sku, branch, journal, average_sales_per_hour, hours_open, days_open)
        self.assertEqual(calculated_run_rate, expected_run_rate)
        


        
    def test_calculate_missed_revenue(self):
        retail_price = 500
        #do I use run rate in this function or ROS
        journal = [{'Branch':branch, 'Date':sale_1, 'Increment':-1,'Sku':sku,'Tag':'sale'},
                   {'Branch':branch, 'Date':sale_2, 'Increment':10,'Sku':sku,'Tag':'purchase'}]
        #if we assume a constant rate of sales, then we can calculate missed revenue as:
        expected_missed_revenue = low_stock_periods * average_rate_of_sales * retail_price
        #method from MissedRevenueHeatmapGenerator
        calculated_missed_revenue = calculate_missed_revenue(sku, branch, journal, retail_price, low_stock_periods)
        
        self.assertEqual(calculated_missed_revenue, expected_missed_revenue)





if __name__ == '__main__':
    unittest.main()


