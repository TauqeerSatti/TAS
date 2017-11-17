from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure, output_file, output_notebook, show
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.util.string import encode_utf8
from bokeh.plotting import figure, show, output_file
import quandl
import datetime
from dateutil.relativedelta import relativedelta
quandl.ApiConfig.api_key = 'Rxj4nk5yws4PVyy6usDg'

app = Flask(__name__)
app.vars ={}
Company= []
data =[]
Plots= []
Colors =['orange','green','red', 'blue']
start_date = (datetime.datetime.today() - relativedelta(months=1)).strftime('%Y-%m-%d')
end_date   = datetime.datetime.today().strftime('%Y-%m-%d')
@app.route('/')
def index():
    return render_template('index.html')
		

		
@app.route('/plot', methods =['POST'])
def plot1():
    Company = request.form['Company']
    Plots=request.form.getlist('answer_from_user')
    
    
	
    if (not Company): return render_template('end.html')
    if (not Plots): return render_template('end.html')	
    
    data = quandl.get_table('WIKI/PRICES',date={'gte': start_date,'lt':end_date},ticker = [Company] \
                        , qopts={'columns':['ticker','date','open','close','adj_open','adj_close']})
    Company_data = data[['date','open','close','adj_open','adj_close']]
    Company_data.loc['date'] = pd.to_datetime(Company_data.date)
    Company_data.set_index('date', inplace=True)
    p = figure(x_axis_type="datetime", plot_width=1000, plot_height=600, title='Quandl Wiki Stock Prices - {}'.format(Company))
    p.xaxis.axis_label = "Dates"
    p.xaxis.axis_line_width = 1
    
    p.yaxis.axis_label = "Prices ($)"
    p.yaxis.axis_line_width = 1

    x=0
    for x in range(len(Plots)):
        p.line(Company_data.index,  Company_data[Plots[x]], color= Colors[x], legend= Plots[x] , line_width= 0.75 )
        x = x+1
        
    p.legend.location = 'top_left'
    # render template
    script, div = components(p)
    html=render_template('plot.html', script=script, div=div)
    return encode_utf8(html)

if __name__ == '__main__':
  #app.run(host='0.0.0.0')
  app.run(port=33507)

#port = int(os.environ.get('PORT', 5000))
#    app.run(host='0.0.0.0', port=port)