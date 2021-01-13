import mechanize
from datetime import datetime

def fetch_expiry_dates():

    print('Fetching expiry dates from iCharts...')

    br = mechanize.Browser()
    br.open('https://options.icharts.in/opt/login.php')

    # Perform Login
    br.select_form(name='login')
    br.form['username'] = '#'
    br.form['password'] = '#'
    br.submit()

    # Select Historical Data
    br.open('https://options.icharts.in/opt/OptionChain.php')
    br.select_form(id='frmOptChain')
    br.form['rdDataType'] = ['hist']
    br.submit()

    # Extract Expiry Dates
    br.select_form(id='frmOptChain')
    select_control = br.form.find_control('optExpDate_hist')
    expiry_dates = [item.attrs['value'].title() for item in select_control.items]

    # Convert into python date objects
    expiry_dates = [datetime.strptime(dt, '%d%b%y').date() for dt in expiry_dates]

    print('Done')

    return sorted(expiry_dates)

if __name__ == '__main__':
    print(fetch_expiry_dates())