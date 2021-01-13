import requests
from datetime import date

# Check if a number can be converted into a float
def is_float(num: str) -> bool:
        try:
            float(num)
            return True
        except ValueError:
            return False
        except TypeError:
            return False

# Class to perform the actual request and parsing of response of option chain data.
class OptionScraper:
    def _parse_response(self, data: dict) -> dict:
        response = []
        for row in data:
            row = [x if x != '-' else None for x in row]
            row = [float(x) if is_float(x) else x for x in row]

            call_data = {
                'IV': row[8],
                'OI': row[10],
                'OI Change': row[9],
                'Volume': row[11],
                'LTP': row[13],
            }

            put_data = {
                'IV': row[26],
                'OI': row[24],
                'OI Change': row[25],
                'Volume': row[23],
                'LTP': row[21],
            }

            response.append({
                'Call': call_data,
                'Strike Price': row[17],
                'Put': put_data
            })
        
        return response

    def get_options_data(self, stock: str, current_date: date, expiry_date: date):

        current_date = current_date.strftime('%Y-%m-%d')
        expiry_date = expiry_date.strftime('%d%b%y').upper()
    
        url = f'https://options.icharts.in/opt/OptionChainTable.php?txtDate={current_date}&optSymbol={stock}&optExpDate={expiry_date}&dType=hist&striketype=allstrikes'
   
        response = requests.request("POST", url, headers={
            'Referer': 'https://options.icharts.in/opt/OptionChain.php'
        }).json()
        
        return self._parse_response(response['aaData'])
