from datetime import datetime, timedelta, date
from collections import defaultdict
from scraper import OptionScraper
import json

class OptionChainData:
    def __init__(self, stock_name: str, first_expiry_date: date, last_expiry_date: date = None):
        self.expiry_dates = self._generate_expiry_dates(first_expiry_date, last_expiry_date)
        self.stock_name = stock_name
        self.scraper = OptionScraper()

    def _generate_expiry_dates(self, start_date: date, end_date: date = None) -> list[date]:
        current = start_date
        expiry_dates = defaultdict(list)

        if not end_date:
            end_date = date(start_date.year + 1, 1, 1)
        
        expiry_dates[start_date.month].append(start_date)

        while (current := current + timedelta(weeks=1)) < end_date:
            expiry_dates[current.month].append(current)

        return expiry_dates

    # def _load_data(self, current_date: date):
    #     return self.scraper.get_options_data(self.stock_name, current_date, expiry_date)

if __name__ == '__main__':

    scraper = OptionScraper()
    current_date = date(2019, 12, 26)
    expiry_date = date(2020, 1, 2)
    data = scraper.get_options_data('BANKNIFTY', current_date, expiry_date)
    
    print(len(data))