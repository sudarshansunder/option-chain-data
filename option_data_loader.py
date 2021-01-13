from datetime import datetime, timedelta, date
from scraper import OptionScraper
import json

def generate_expiry_dates(start_date: date, end_date: date = None):
        current = start_date
        expiry_dates = [start_date]
        # Final expiry date for every month
        final_expiry_dates = {}

        final_expiry_dates[current.month] = current

        if not end_date:
            end_date = date(start_date.year + 1, 1, 1)

        while (current := current + timedelta(weeks=1)) < end_date:
            expiry_dates.append(current)
            final_expiry_dates[current.month] = current

        return expiry_dates, final_expiry_dates

def format_date(x: date):
    return x.strftime('%d%b%y').upper()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

class OptionDataLoader:
    def __init__(self, stock_name: str, first_expiry_date: date, last_expiry_date: date = None):
        self.first_expiry_date = first_expiry_date
        self.last_expiry_date = last_expiry_date
        self.expiry_dates, self.final_expiry_dates = generate_expiry_dates(first_expiry_date, last_expiry_date)
        self.stock_name = stock_name
        self.scraper = OptionScraper()

    def _get_current_expiry_date(self, current_date: date, prev_expiry_date: date = None) -> date:
        if prev_expiry_date:
            if current_date >= prev_expiry_date:
                current_expiry_idx = self.expiry_dates.index(prev_expiry_date)
                return self.expiry_dates[current_expiry_idx+1] if current_expiry_idx + 1 < len(self.expiry_dates) else None
            else:
                return prev_expiry_date

        #TODO: Implement binary search to find the current expiry date for given date.

    def _load_data_for_date(self, target_date: date, current_expiry_date: date):
        # return self.scraper.get_options_data(self.stock_name, target_date, expiry_date)
        next_expiry_date = self.expiry_dates[self.expiry_dates.index(current_expiry_date) + 1]
        month_end_expiry_date = self.final_expiry_dates[next_expiry_date.month]

        options_data = {
            format_date(current_expiry_date): self.scraper.get_options_data(self.stock_name, target_date, current_expiry_date),
            format_date(next_expiry_date): self.scraper.get_options_data(self.stock_name, target_date, next_expiry_date),
        }

        if next_expiry_date == month_end_expiry_date:
            options_data[format_date(month_end_expiry_date)] = None
        else:
            options_data[format_date(month_end_expiry_date)] = self.scraper.get_options_data(self.stock_name, target_date, month_end_expiry_date)

        return options_data

    def load_data(self, start_date: date, end_date: date):
        current_expiry = self.first_expiry_date
        options_data = {}
        for dt in daterange(start_date, end_date):
            current_expiry = self._get_current_expiry_date(dt, current_expiry)
            options_data[format_date(dt)] = self._load_data_for_date(dt, current_expiry)

        return options_data
        