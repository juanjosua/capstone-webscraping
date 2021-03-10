from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup
import requests

# don't change this
matplotlib.use('Agg')
app = Flask(__name__)  # do not change this

# insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content, "html.parser")

table = soup.find('table', attrs={
                  'class': 'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr', attrs={'class': None})
temp = []  # initiating a tuple

for i in range(1, len(tr)):
    #scrapping process
    row = table.find_all('tr', attrs={'class': None})[i]
    
    #get date
    date = row.find_all('td')[0].text
    date = date.strip() #for removing the excess whitespace
    
    #get exchange rates
    xc_rate = row.find_all('td')[2].text
    xc_rate = xc_rate.strip() #for removing the excess whitespace
    
    temp.append((date, xc_rate))
    
temp

# change into dataframe
data = pd.DataFrame(temp, columns=('date', 'exchange_rates'))

# insert data wrangling here
data['exchange_rates'] = data['exchange_rates'].str.replace(' IDR','')
data['exchange_rates'] = data['exchange_rates'].str.replace(',','')
data['exchange_rates'] = data['exchange_rates'].astype('float64')
data['date'] = data['date'].astype('datetime64')

# end of data wranggling


@app.route("/")
def index():

    card_data = f'{data["exchange_rates"].mean().round(2)} IDR'

    # generate plot
    plt.plot(data['date'], data['exchange_rates'], linestyle='-', label='IDR/USD')
    plt.xlabel('Date Period')
    plt.ylabel('Exchange Rates (IDR)') 
    plt.title('Indonesian Rupiahs (IDR) per US Dollar (USD)')
    plt.legend()

    # Rendering plot
    # Do not change this
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_result = str(figdata_png)[2:-1]

    # render to html
    return render_template('index.html', card_data=card_data, plot_result=plot_result)


if __name__ == "__main__":
    app.run(debug=True)
