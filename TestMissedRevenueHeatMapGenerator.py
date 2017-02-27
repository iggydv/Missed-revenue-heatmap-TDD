import datetime, time
import unittest
import MissedRevenueHeatmapGenerator

MR = MissedRevenueHeatmapGenerator.MissedRevenueHeatmapGenerator()


# Methods in the MissedRevenueHeatmapGenerator class
# ============================================================================================================================================

# calculate_stock_level(self,sku, branch, journal, stock_level):
# return the stock levels of certain sku at a branch

# calculate_danger_periods(self, sku, branch, danger_level, stock_level):

# calculate_average_rate_of_sale_per_hour(self,sku, branch, journal, business_hours, date_range):

# calculate_run_rate(self,sku, branch, journal, rate_of_sale_per_hour, business_hours_per_day):

# calculate_missed_revenue(self, sku, branch, journal, retail_price, danger_period):

# ============================================================================================================================================

# All unittests were written under the following assumptions:
#   (1) testing functions for one product(sku) at one branch
#   (2) parsing of csv files are errorless
#   (3) constant rate of sale for any product at any branch
#   (4) business hours for a branch is 9am - 5pm (8 hours)

class TestMissedRevenueHeatmapGenerator(unittest.TestCase):
    # ============================================================================================================================================
    sku = 'FON6-TPD-WHT'
    branch = 'Cape Town'
    # use cape town branch business hours
    # what about public holidays?
    # closed on sunday
    normal_business_hours = ['9am', '5pm']
    weekend_business_hours = ['9am', '1pm']

    business_hours = {'monday': normal_business_hours,
                      'tuesday': normal_business_hours,
                      'wednesday': normal_business_hours,
                      'thursday': normal_business_hours,
                      'friday': normal_business_hours,
                      'saturday': weekend_business_hours}
    # list of branches and their business hours
    branch_info = [{'Branch': branch, 'Business hours': business_hours}]

    time_branch_opens = datetime.datetime(2017, 1, 3, 9)
    time_branch_closes = datetime.datetime(2017, 1, 3, 17)

    one_week_later = time_branch_opens + datetime.timedelta(days=7)
    # 3rd Jan - 3rd Feb is 31 days
    one_month_later = time_branch_opens + datetime.timedelta(days=31)

    sale_date_1 = time_branch_opens + datetime.timedelta(hours=1)
    sale_date_2 = time_branch_opens + datetime.timedelta(hours=5)
    purchase_date_1 = time_branch_opens + datetime.timedelta(hours=2)
    purchase_date_2 = time_branch_opens + datetime.timedelta(hours=7)

    # ============================================================================================================================================
    def test_calculate_hours_a_branch_is_open_per_day(self):
        '''Test the calculated amount of hours a branch is open'''
        day_of_the_week = 'monday'
        # TODO: test for sundays/public holidays
        # extract information from branch_info dict
        expected_hours_open = 8
        calculated_hours_open = MR.calculate_hours_a_branch_is_open_per_day(self.branch, day_of_the_week,
                                                                            self.branch_info)

        self.assertEqual("calculate_hours_a_branch_is_open_per_day() returned incorrect value", calculated_hours_open,
                         expected_hours_open)

    def test_calculate_stock_level_for_sku_at_specific_branch_for_a_period(self):
        '''Test the calculated amount of stock for a sku at a branch'''
        # need sales and purchases to change stock level

        # test time period is one day
        time_period = (self.time_branch_opens, self.time_branch_closes)
        initial_stock_level = 500

        journal = [{'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -1, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_1, 'Increment': 3, 'Sku': self.sku,
                    'Tag': 'purchase'},
                   {'Branch': self.branch, 'Date': self.sale_date_2, 'Increment': -2, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_2, 'Increment': 5, 'Sku': self.sku,
                    'Tag': 'purchase'}]

        # Extacted sales/purchases within the given time period
        # 500 - 1 + 3 - 2 + 5
        expected_stock_level = 505
        calculated_stock_level = MR.calculate_stock_level_for_sku_at_specific_branch_for_a_period(self.sku,
                                                                                                       self.branch,
                                                                                                       time_period,
                                                                                                       journal,
                                                                                                       initial_stock_level)

        self.assertEqual("calculate_stock_level_for_sku_at_specific_branch_for_a_period() returned incorrect value", calculated_stock_level,
                         expected_stock_level)

    def test_calculate_low_stock_level_periods(self):
        '''Calculate the periods in time for which stock level was below the danger level.
           The danger level is defined as the stock level at which customers don’t buy.
           The danger period is defined as a period of time where stock level is equal or less than danger level.'''
        # define a journal to simulate low stock level periods
        journal = [{'Branch': self.branch, 'Date': self.time_branch_opens, 'Increment': 10, 'Sku': self.sku,
                    'Tag': 'purchase'},
                   {'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -10, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_1, 'Increment': 1, 'Sku': self.sku,
                    'Tag': 'purchase'},
                   {'Branch': self.branch, 'Date': self.sale_date_2, 'Increment': -1, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_2, 'Increment': 20, 'Sku': self.sku,
                    'Tag': 'purchase'}]
        # there are two periods during which stock is 0
        danger_period_1 = (self.sale_date_1, self.purchase_date_1)
        danger_period_2 = (self.sale_date_2, self.purchase_date_2)

        # return a tuple with time periods when stock was zero
        calculated_danger_period = MR.calculate_low_stock_level_periods(self.sku, self.branch, journal)

        self.assertEqual("calculated_danger_period() returned incorrect value", calculated_danger_period,
                         [danger_period_1, danger_period_2])

        # test with danger_level = 1
        # TODO: Create seperate tests for varying danger levels
        danger_period_3 = (self.sale_date_1, self.purchase_date_2)
        calculated_danger_period = MR.calculate_low_stock_level_periods(self.sku, self.branch, journal, 1)

        self.assertEqual("calculate_low_stock_level_periods() returned incorrect value", calculated_danger_period,
                         (danger_period_3,))

    # TODO: Add test to ensure that low_stock_level_periods is always within business hours

    def test_calculate_average_rate_of_sale_per_hour_for_a_period(self):
        '''Test the calculated average hourly rate of sale for one day'''
        # TODO: Calculate average rate for larger periods
        time_period = (self.time_branch_opens, self.time_branch_closes)  # one day
        # 3 Jan 2017 was a Tuesday
        # could be extracted from calculate_hours_a_branch_is_open_per_day()
        hours_open = 8
        journal = [{'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -6, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_1, 'Increment': 2, 'Sku': self.sku,
                    'Tag': 'purchase'},
                   {'Branch': self.branch, 'Date': self.sale_date_2, 'Increment': -7, 'Sku': self.sku, 'Tag': 'sale'}]
        # Count all sales within the time period
        # increment of sales is negative
        # sales = 6 + 7
        sales = 13
        expected_average_rate_of_sale_per_hour = sales / hours_open
        calculated_average_rate_of_sale_per_hour = MR.calculate_average_rate_of_sale_per_hour_for_a_period(self.sku,
                                                                                                           self.branch,
                                                                                                           journal,
                                                                                                           hours_open,
                                                                                                           time_period)
        self.assertEqual("calculate_average_rate_of_sale_per_hour_for_a_period() returned incorrect value",
                         calculated_average_rate_of_sale_per_hour, expected_average_rate_of_sale_per_hour)

    def test_calculate_lost_qty_sales_for_a_period(self):
        '''Test the calculated quantity of lost sales for a period.'''

        # TODO: reuse to calculate monthly/quaterly/yearly run rate
        journal = [{'Branch': self.branch, 'Date': self.time_branch_opens, 'Increment': 10, 'Sku': self.sku,
                    'Tag': 'purchase'},
                   {'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -10, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_1, 'Increment': 1, 'Sku': self.sku,
                    'Tag': 'purchase'}]

        # TODO: Create a function to calculate amount of business hours in a period
        time_period = (self.time_branch_opens, self.time_branch_closes)
        amount_of_hours = 8
        # stock level fell below/equal danger level for 1 hour during this time period
        danger_period_within_time_period = 1
        amount_of_sales = 10
        # average_rate_of_sale_per_hour = 10 sales / 8 hours
        average_rate_of_sale_per_hour = amount_of_sales / amount_of_hours
        qty_of_lost_sales = danger_period_within_time_period * average_rate_of_sale_per_hour

        calculated_qty_of_lost_sales = MR.test_calculate_lost_qty_sales_for_a_period(self.sku, self.branch, journal,
                                                                                     time_period,
                                                                                     average_rate_of_sale_per_hour)
        self.assertEqual("calculate_lost_qty_sales_for_a_period() returned incorrect value", calculated_qty_of_lost_sales,
                         qty_of_lost_sales)

    def test_calculate_run_rate_for_a_week(self):
        '''Test the calculated run rate of lost sales for a period.
           Run rate is used to extrapolate data, in this case amount of sales, to predict quantity of future sales'''
        # define one week period
        period = (self.time_branch_opens, self.one_week_later)

        journal = [{'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -6, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.sale_date_2, 'Increment': -10, 'Sku': self.sku, 'Tag': 'sale'}]

        # calculate average_sales_per_hour for one day: 16 sales / 8 hours
        # TODO: extend calculate average sales function, to calculate average sales for a week/month/year/etc
        average_sales_per_hour = 2

        hours_open_weekday = 8
        hours_open_weekend = 4
        # to calculate the weekly run rate, I extrapolate the average sales per hour to a week
        expected_weekly_run_rate = average_sales_per_hour * (hours_open_weekday * 5 + hours_open_weekend * 1)

        # get run rate for the defined period
        calculated_weekly_run_rate = MR.calculate_run_rate(self.sku, self.branch, journal, period)
        self.assertEqual("calculated_run_rate() returned incorrect value", calculated_weekly_run_rate,
                         expected_weekly_run_rate)

    def test_calculate_run_rate_for_a_month(self):
        '''Test the calculated run rate of lost sales for a period.
           Run rate is used to extrapolate data, in this case amount of sales, to predict quantity of future sales'''
        # define one week period
        period = (self.time_branch_opens, self.one_month_later)

        journal = [{'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -6, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.sale_date_2, 'Increment': -10, 'Sku': self.sku, 'Tag': 'sale'}]

        # calculate average_sales_per_hour for one day: 16 sales / 8 hours
        # TODO: extend calculate average sales function, to calculate average sales for a week/month/year/etc
        average_sales_per_hour = 2

        hours_open_weekday = 8
        hours_open_weekend = 4
        # to calculate the weekly run rate, I extrapolate the average sales per hour to a week
        expected_monthly_run_rate = average_sales_per_hour * (hours_open_weekday * 20 + hours_open_weekend * 4)

        # get run rate for the defined period
        calculated_monthly_run_rate = MR.calculate_run_rate(self.sku, self.branch, journal, period)
        self.assertEqual("calculated_run_rate() returned incorrect value", calculated_monthly_run_rate,
                         expected_monthly_run_rate)

    def test_calculate_missed_revenue(self):
        '''Test calculated missed revenue for a certain sku at a branch
           Missed revenue equals, missed quantity of sales, multiplied by the retail price of the item'''

        time_period = (self.time_branch_opens, self.time_branch_closes)

        journal = [{'Branch': self.branch, 'Date': self.time_branch_opens, 'Increment': 10, 'Sku': self.sku,
                    'Tag': 'purchase'},
                   {'Branch': self.branch, 'Date': self.sale_date_1, 'Increment': -10, 'Sku': self.sku, 'Tag': 'sale'},
                   {'Branch': self.branch, 'Date': self.purchase_date_1, 'Increment': 1, 'Sku': self.sku,
                    'Tag': 'purchase'}]

        # calculate hourly rate of sale over the specific time period
        time_period_in_hours = 8
        sales = 10
        average_rate_of_sale_per_hour = sales / time_period_in_hours

        # calculate the lost sales from journal
        qty_of_lost_sales = MR.test_calculate_lost_qty_sales_for_a_period(self.sku, self.branch, journal, time_period,
                                                                          average_rate_of_sale_per_hour)
        retail_price = 500

        expected_missed_revenue = qty_of_lost_sales * retail_price
        # calculate missed revenue from journal
        calculated_missed_revenue = MR.calculate_missed_revenue(self.sku, self.branch, retail_price, journal,
                                                                time_period)

        self.assertEqual("calculate_missed_revenue() returned incorrect value", calculated_missed_revenue,
                         expected_missed_revenue)


if __name__ == '__main__':
    unittest.main()
