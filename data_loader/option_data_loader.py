from datetime import datetime, timedelta, date
from data_loader.scraper import OptionScraper
from collections import defaultdict
import json
from data_loader.expiry_dates import fetch_expiry_dates

def generate_expiry_dates(start_date: date, end_date: date = None):
        fetched_expiry_dates = fetch_expiry_dates()
        current_idx = fetched_expiry_dates.index(start_date)
        expiry_dates = []
        # Final expiry date for every month
        final_expiry_dates = defaultdict(dict)

        if not end_date:
            end_date = date(start_date.year + 1, 2, 1)

        while current_idx < len(fetched_expiry_dates):
            current = fetched_expiry_dates[current_idx]
            if current >= end_date:
                break
            expiry_dates.append(current)
            final_expiry_dates[current.year][current.month] = current
            current_idx += 1

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
            if current_date > prev_expiry_date:
                current_expiry_idx = self.expiry_dates.index(prev_expiry_date)
                return self.expiry_dates[current_expiry_idx+1] if current_expiry_idx + 1 < len(self.expiry_dates) else None
            else:
                return prev_expiry_date

        #TODO: Implement binary search to find the current expiry date for given date.

    def _load_data_for_date(self, target_date: date, current_expiry_date: date):
        # return self.scraper.get_options_data(self.stock_name, target_date, expiry_date)
        next_expiry_date = self.expiry_dates[self.expiry_dates.index(current_expiry_date) + 1]
        month_end_expiry_date = self.final_expiry_dates[next_expiry_date.year][next_expiry_date.month]

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
        