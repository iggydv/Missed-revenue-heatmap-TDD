class DataExtractor:
    #METHODS
    #====================================================================
    def calculate_missed_revenue_at_branch_for_sku_between(sku, branch, date_range, journal, danger_level=0):
        # TODO: implement this
        pass
    
    def calculate_rate_of_sale(sku, branch, date_range, journal):
        #TODO: implement this
        pass

    def calculate_stock_level(sku, timestamp, branch, journal):
        #TODO: implement this
        pass

    def calculate_rate_of_sales_over_time(journal, date_range, aggregation_fn):
        #TODO: implement this
        pass

    def calculate_danger_level():
        #TODO: implement this
        pass

    def calculate_daily_missed_revenue_for_sku():
        #TODO: implement this
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
