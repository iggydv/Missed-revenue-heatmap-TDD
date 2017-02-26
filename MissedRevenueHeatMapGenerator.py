class MissedRevenueHeatmapGenerator:

    #METHODS
    #====================================================================
    def calculate_hours_a_branch_is_open(self, branch, day_of_the_week, business_hours_dict):
        '''return the hours (integer) a branch is open'''
        #TODO: Implement this
        #return hours a branch is open
        pass

    def calculate_low_stock_level_periods(self, sku, branch, journal, danger_level=0):
        #TODO: Implement this
        #this function will output the amount of time (integer) for which the stock_level
        #was below the danger level.
        pass

    def calculate_average_rate_of_sale_per_hour(self,sku, branch, journal, hours_open):
        #TODO: Implement this
        #return average rate of sale for a day per hour
        pass

    def test_calculate_lost_qty_sales_for_a_period(self, sku, branch, journal, time_period, average_rate_of_sale_per_hour):
        #TODO: Implement this
        #return qty of lost sales for a time period
        pass
        
    def calculate_run_rate(self, sku, branch, journal, period):
        #TODO: Implement this
        #return run rate for a period
        pass
    
    def calculate_missed_revenue(self, sku, branch, expected_missed_revenue, qty_of_lost_sales):
        #TODO: Implement this
        #return missed revenue
        pass
    
    def test_calculate_stock_level_for_sku_at_specific_branch(self,sku, branch, journal, stock_level):
        #TODO: Implement this
        #Extract sales and purchases in order to increment/decrement the stock level
        #return stock level
        pass
    
    #====================================================================

    #UTILITY FUNCTIONS
    #====================================================================
    def _extract_date(self, journal):
        # TODO: implement this
        pass
    
    def _extract_branch(self, journal):
        # TODO: implement this
        pass
    
    def _extract_increment(self, journal):
        # TODO: implement this
        pass
    
    def _extract_sku(self, journal):
        # TODO: implement this
        pass

    def _extract_tag(self, journal):
        # TODO: implement this
        pass
    #====================================================================

