import requests
from datetime import datetime
import json

schema = {
    'calls': ['Build Up', 'Trend', 'Time', 'Vega', 'Theta', 'Gamma', 'Delta', 'IV Chg', 'IV', 'OI Chg', 'OI', 'Volume', 'Chg (Pts)', 'LTP'],
    'puts': ['LTP', 'Chg (Pts)', 'Volume', 'OI', 'OI Chg', 'IV', 'IV Chg', 'Delta', 'Gamma', 'Theta', 'Vega', 'PCR-OI', 'PCR-Vol', 'Time', 'Trend', 'Build Up']
}

def is_float(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def parse_response(data: dict) -> dict:
    response = []
    for row in data:
        row = [x if x != '-' else None for x in row]
        row = [float(x) if is_float(x) else x for x in row]
        calls_data = dict(zip(schema['calls'], row[:15]))
        puts_data = dict(zip(schema['puts'], row[16:]))
        response.append({
            'Calls': calls_data,
            'Strike Price': row[15],
            'Puts': puts_data
        })
    
    return response

if __name__ == '__main__':

    stock_name = 'NIFTY'
    current_date = datetime.now().strftime('%Y-%m-%d')


    url = f'https://options.icharts.in/opt/OptionChainTable.php?txtDate={current_date}&optSymbol={stock_name}&optExpDate=24DEC20&dType=latest&striketype=allstrikes'

    response = requests.request("POST", url, headers={}, data={})
    nifty_data = response.json()
    stock_data = parse_response(nifty_data['aaData'])

    print(len(stock_data))

    #print(json.dumps(stock_data, indent=2))