from datetime import date
from option_data_loader import OptionDataLoader
import json

if __name__ == '__main__':

    start_date = date(2020, 1, 1)
    end_date = date(2020, 1, 4)
    expiry_date = date(2020, 1, 2)
    
    loader = OptionDataLoader('BANKNIFTY', expiry_date)
    data = loader.load_data(start_date, end_date)

    with open('stock_dump.json', 'w') as fp:
        json.dump(data, fp, indent=2)