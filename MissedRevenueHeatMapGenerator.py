class MissedRevenueHeatmapGenerator:

    #METHODS
    #====================================================================
    def calculate_business_hours(self, branch_dict):
        #TODO: Implement this
        pass

    def calculate_danger_periods(self, sku, branch, danger_level, stock_level):
        #TODO: Implement this
        #this function will output the amount of time (integer) for which the stock_level
        #was below the danger level.
        pass

    def calculate_average_rate_of_sale_per_day(self,sku, branch, journal, business_hours, date_range):
        #TODO: Implement this
        pass
    
    def calculate_run_rate(self,sku, branch, journal, rate_of_sale_per_hour, business_hours_per_day):
        #TODO: Implement this
        pass
    
    def calculate_missed_revenue(self, sku, branch, journal, retail_price, danger_period):
        #TODO: Implement this
        pass
    
    def calculate_stock_level(self,sku, branch, journal, stock_level):
        #TODO: Implement this
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

