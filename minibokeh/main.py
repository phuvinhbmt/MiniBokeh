# script to implement Bokeh
from scripts.plot_tab import plot_tab

# Bokeh basic functions
from bokeh.models.widgets import Tabs
from bokeh.models import CategoricalColorMapper
from bokeh.layouts import row, column, widgetbox
from bokeh.io import curdoc, show, output_file
from urllib.error import URLError

# functions to import dataset
import pandas as pd
from os.path import dirname, join

# Import dataset
try: # retrieve dataset from online resource 
    url = 'https://assets.datacamp.com/production/repositories/401/datasets/09378cc53faec573bcb802dce03b01318108a880/gapminder_tidy.csv' 
    data = pd.read_csv(url,  index_col = 'Year' )
except URLError: # if url is down, import from local csv file
    print('Online dataset is broken. Retrieve it locally')
    data = pd.read_csv(join(dirname(__file__), 'data', 'fertilities.csv'), index_col = 'Year')

# plot and add it to document
layout = plot_tab(data)
curdoc().add_root(layout)