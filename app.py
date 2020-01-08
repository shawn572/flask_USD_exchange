from flask import Flask, render_template, request, redirect
import requests
from pandas import *
import json
from bokeh.io import show,output_file
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

app = Flask(__name__)

c = requests.get('http://www.apilayer.net/api/live?access_key=7be4fc46c8271fa102d20a0b3306747e')
c = json.loads(c.text)
df = DataFrame(c)
conversion = df['quotes']
currencys = []
for i in conversion.index:
    currencys.append(i)
rates = []
for j in conversion.array:
    rates.append(j)

app.vars = {}

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        app.vars = request.form['currency2']
        return redirect('/result')

@app.route('/result')
def result():
    currency = 'USD'+str(app.vars)
    if currency in currencys:
        source = ColumnDataSource(data=dict(currency_plot=currencys[:10],\
                                            rate_plot=rates[:10]))
        p = figure(x_range=currencys[:10],title="First 10 (alphabetically) USD exchange rate up-to-date")
        p.vbar(x='currency_plot',top='rate_plot',width=0.1,source=source)
        p.xaxis.axis_label = None
        p.yaxis.axis_label = "Exchagne rate (based on 1 USD)"
        output_file("USDExchangeRate.html")
        show(p)
        return render_template('about.html',rate=conversion[currency])
    return render_template('end.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
