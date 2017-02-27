class MissedRevenueHeatmapGenerator:

    #METHODS
    #====================================================================
    def calculate_hours_a_branch_is_open_per_day(self, branch, day_of_the_week, branch_info):
        '''return's the hours (integer) a branch is open'''
        #find business_hours for the specific branch in the branch info dict
        #TODO: Implement this
        #return hours_open_per_day
        pass

    def calculate_low_stock_level_periods(self, sku, branch, journal, danger_level=0):
        '''return's a list of tuples, which represent periods in time, for which stock level of a sku at a branch was below the danger level'''
        #each period tuple contains a start date and end date, which effectively is the opening and the closing of the
        #low stock level period.
        #TODO: Implement this
        #return list_low_stock_level_periods
        pass

    def calculate_average_rate_of_sale_per_hour_for_a_period(self, sku, branch, journal, hours_open, time_period):
        '''return's the average rate of sale of a sku at a specific branch in sales per hour'''
        #TODO: Implement this
        #return average_rate_of_sale_per_hour
        pass

    def test_calculate_lost_qty_sales_for_a_period(self, sku, branch, journal, time_period, average_rate_of_sale_per_hour):
        '''return qty of lost sales on a sku at a branch for a certain time period'''
        #TODO: Implement this
        #return lost_qty_sales
        pass
        
    def calculate_run_rate(self, sku, branch, journal, period):
        '''return run rate of a sku at a certain branch for a certain period'''
        #TODO: Implement this
        #return run_rate
        pass
    
    def calculate_missed_revenue(self, sku, branch, retail_price, journal, time_period):
        '''return's the missed revenue amount of a sku at a branch for a certain period in time'''
        #TODO: Implement this
        #return missed_revenue
        pass
    
    def calculate_stock_level_for_sku_at_specific_branch_for_a_period(self, sku, branch, time_period, journal, stock_level):
        '''Extract sales and purchases in order to increment/decrement the stock level
           return's the stock level of a sku at a branch'''
        #TODO: Implement this
        #TODO: function should extract sales/purchases within the specific time_period
        #return stock_level
        pass
    
    #====================================================================

    #UTILITY FUNCTIONS
    #====================================================================
    def _extract_date(self, journal):
        '''Extract date & time of journal entries'''
        # TODO: implement this
        #return date
        pass
    
    def _extract_branch(self, journal):
        '''Extract branch name of journal entries'''
        # TODO: implement this
        #return branch_name
        pass
    
    def _extract_increment(self, journal):
        '''Extract stock influencer 'increment' of journal entries'''
        # TODO: implement this
        #return increment
        pass
    
    def _extract_sku(self, journal):
        '''Extract sku of journal entries'''
        # TODO: implement this
        #return sku
        pass

    def _extract_tag(self, journal):
        '''Extract tag of journal entries'''
        # TODO: implement this
        #return tag
        pass
    #====================================================================

