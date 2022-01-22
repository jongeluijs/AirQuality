"""
This script retrieves the Gas and Elec usage from yesterday from
my slimme-meter and put's the results 2 bokeh-graphs in a html-file
"""

import pandas as pd
import datetime
import time
import sqlite3
from bokeh.plotting import figure, show, save, output_file, reset_output
from bokeh.layouts import column, row
from bokeh.models import Div, Title, Span


#################### Helper classes

class Database():
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)

    def get_enviro(self, start_ts, end_ts):
        df = pd.read_sql_query("SELECT * FROM environ WHERE timedate > {} and timedate < {}".format(
                         start_ts, end_ts), self.conn)
        return df

    def get_pms5003(self, start_ts, end_ts):
        df = pd.read_sql_query("SELECT * FROM pms5003 WHERE timedate > {} and timedate < {}".format(
            start_ts, end_ts), self.conn)
        return df

    def get_gasses(self, start_ts, end_ts):
        df = pd.read_sql_query("SELECT * FROM gasses WHERE timedate > {} and timedate < {}".format(
            start_ts, end_ts), self.conn)
        return df

################################################

# The tools we want to add to the plots
TOOLS = "box_select, box_zoom, lasso_select,help"
TOOLS = "pan,wheel_zoom,box_zoom,reset"

# Connect database is in my pi-host "slimme-meter"
db = Database('airquality.db')

# Define the period to retrieve the data for
yesterday = (datetime.date.today() - datetime.timedelta(days=1))
end_ts = (datetime.date.today()).strftime('%s')
start_ts = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%s')

# Create Deeltjes plot
pms5003_df = db.get_pms5003(start_ts, end_ts)
pms5003_df['x_axis'] = [datetime.datetime.fromtimestamp(int(x)) for x in pms5003_df.timedate]
temp_title = 'Deeltjes'
p1 = figure(tools=TOOLS, x_axis_type="datetime", title=temp_title, plot_height=350, plot_width=1000)
p1.title.align = 'center'
p1.xgrid.grid_line_color=None
p1.ygrid.grid_line_alpha=0.5
p1.xaxis.axis_label = 'Time'
p1.yaxis.axis_label = 'micro-gram / m3'
p1.line(pms5003_df.x_axis, pms5003_df.pm1, color='black')
p1.circle(pms5003_df.x_axis, pms5003_df.pm1, color='black', size=2)
p1.line(pms5003_df.x_axis, pms5003_df.pm25, color='red')
p1.circle(pms5003_df.x_axis, pms5003_df.pm25, color='red', size=2)
p1.line(pms5003_df.x_axis, pms5003_df.pm10, color='green')
p1.circle(pms5003_df.x_axis, pms5003_df.pm10, color='green', size=2)

# Create the gas figure
gasses_df = db.get_gasses(start_ts, end_ts)
gasses_df['x_axis'] = [datetime.datetime.fromtimestamp(int(x)) for x in gasses_df.timedate]
temp_title = 'Gas'
p2 = figure(tools=TOOLS, x_axis_type="datetime", title=temp_title, plot_height=350, plot_width=1000)
p2.title.align = 'center'
p2.xgrid.grid_line_color=None
p2.ygrid.grid_line_alpha=0.5
p2.xaxis.axis_label = 'Time'
p2.yaxis.axis_label = 'Concentratie'
p2.line(gasses_df.x_axis, gasses_df.oxidising, color='black')
p2.circle(gasses_df.x_axis, gasses_df.oxidising, color='black', size=2)
p2.line(gasses_df.x_axis, gasses_df.reducing, color='red')
p2.circle(gasses_df.x_axis, gasses_df.reducing, color='red', size=2)
p2.line(gasses_df.x_axis, gasses_df.NH3, color='green')
p2.circle(gasses_df.x_axis, gasses_df.NH3, color='green', size=2)

# Create the gas figure
enviro_df = db.get_enviro(start_ts, end_ts)
enviro_df['x_axis'] = [datetime.datetime.fromtimestamp(int(x)) for x in enviro_df.timedate]
temp_title = 'Temperatuur Vochtigheid Geluid'
p3 = figure(tools=TOOLS, x_axis_type="datetime", title=temp_title, plot_height=350, plot_width=1000)
p3.title.align = 'center'
p3.xgrid.grid_line_color=None
p3.ygrid.grid_line_alpha=0.5
p3.xaxis.axis_label = 'Time'
p3.yaxis.axis_label = 'Celsius % Decibel'
p3.line(enviro_df.x_axis, enviro_df.temperature, color='black')
p3.circle(enviro_df.x_axis, enviro_df.temperature, color='black', size=2)
p3.line(enviro_df.x_axis, enviro_df.humidity, color='red')
p3.circle(enviro_df.x_axis, enviro_df.humidity, color='red', size=2)
p3.line(enviro_df.x_axis, enviro_df.noise, color='green')
p3.circle(enviro_df.x_axis, enviro_df.noise, color='green', size=2)

temp_title = 'Licht Luchtdruk'
p4 = figure(tools=TOOLS, x_axis_type="datetime", title=temp_title, plot_height=350, plot_width=1000)
p4.title.align = 'center'
p4.xgrid.grid_line_color=None
p4.ygrid.grid_line_alpha=0.5
p4.xaxis.axis_label = 'Time'
p4.yaxis.axis_label = 'Lux % mBar'
p4.line(enviro_df.x_axis, enviro_df.light, color='black')
p4.circle(enviro_df.x_axis, enviro_df.light, color='black', size=2)
p4.line(enviro_df.x_axis, enviro_df.pressure, color='red')
p4.circle(enviro_df.x_axis, enviro_df.pressure, color='red', size=2)


outfile = "airquality-{}.html".format(yesterday.strftime('%Y%m%d'))
output_file(outfile, title='Airquality: {}'.format(yesterday.strftime('%Y%m%d')))

title = Div(text='<h2>Lucht kwaliteit op {}</h2>'.format(yesterday),
            style={'text-align':'center', 'color':'blue'}, width=1000)

hrule1 = Div(text='<hr>', width=1000)
hrule2 = Div(text='<hr>', width=1000)
hrule3 = Div(text='<hr>', width=1000)
hrule4 = Div(text='<hr>', width=1000)

show(column(title, hrule1, p1, hrule2, p2, hrule3, p3, hrule4, p4))