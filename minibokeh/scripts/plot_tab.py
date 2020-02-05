# Plotting with Bokeh
from bokeh.models import (
    ColumnDataSource,
    CategoricalColorMapper,
    Slider,
    Select,
    CheckboxGroup,
    HoverTool,
)
from bokeh.plotting import figure
from bokeh.layouts import column, row, widgetbox
from bokeh.io import show, output_file, curdoc
import pandas as pd
DEFAULT_YEAR = 1970

def plot_tab(data):
    def make_dataset(x, y, year, selected_regions )  : # make a new columndatasource 

        by_region_data = pd.DataFrame()
        for reg in selected_regions:
            subset = data[data['region'] == reg]
            by_region_data = by_region_data.append(subset)

        new_src = ColumnDataSource({
            'x': by_region_data.loc[year, x],
            'y': by_region_data.loc[year, y],
            'region': by_region_data.loc[year, 'region'],
        })
        return new_src

    def make_plot(src, mapper): #draw plot with given data column source 
        # create blank figure
        plot = figure(x_axis_label =  x_dropdown.value, y_axis_label = y_dropdown.value, plot_height = 400, plot_width = 700)
        # add cirle point 
        plot.circle(source = src, color = dict(field = 'region', transform = mapper), x = 'x', y = 'y', legend = 'region')
        # add hovertool
        hover = HoverTool(tooltips = [(x_dropdown.value, '@x'), (y_dropdown.value, '@y')])
        plot.add_tools(hover)
        return plot 

    def update(attr, old, new): # function to update plot based on user selection
        yr = slider.value # get value of year slider
        x_value = x_dropdown.value # get value of x_axis drop down
        y_value = y_dropdown.value # get value of y_axis drop down

        selected_region = [region_selection.labels[i] for i in region_selection.active]
        
        # update dataset columnsource based on user input
        new_src = make_dataset(x = x_value, y = y_value, year = yr, selected_regions = selected_region ) 
        # if no regions are selected, display plot with previously selected region 
        if not selected_region:
            print('No regions selected')
        else :
            source.data.update(new_src.data)

        # update x,y axis label 
        plot.xaxis.axis_label = x_value
        plot.yaxis.axis_label = y_value

        # update tooltip of hover tool 
        plot.hover.tooltips = [(x_dropdown.value, '@x'), (y_dropdown.value, '@y')]

    # Color mapper:
    color_values = ['green', 'red', 'blue', 'orange', 'purple', 'pink'] # list of color
    mapper = CategoricalColorMapper(factors = data['region'].unique(), palette = color_values) # make a color mapper for each unique value in column 'region'

    # Slider to select year
    yr_list = (data.index.unique().tolist()) #transform index to a list of years
    slider = Slider(title = 'year', start = yr_list[0], end = yr_list[-1], step = 1, value = DEFAULT_YEAR)
    slider.on_change('value', update)  

    # drop down menu for x axis
    x_dropdown = Select(title = 'x-axis data', options = ['fertility', 'life', 'child_mortality', 'gdp'], value = 'fertility') 
    x_dropdown.on_change('value', update)

    # drop down menu for y axis
    y_dropdown = Select(title = 'y-axis data', options = ['fertility', 'life', 'child_mortality', 'gdp'], value = 'life')
    y_dropdown.on_change('value', update)

    # check box for region 
    region_list = data['region'].unique().tolist()
    region_selection = CheckboxGroup(labels =  region_list, active = [0,1])
    region_selection.on_change('active', update)

    # make a default dataset 
    source = make_dataset(x = 'child_mortality', y = 'life', year = DEFAULT_YEAR, selected_regions= [region_selection.labels[i] for i in region_selection.active] )

    plot = make_plot(source, mapper)
    widget_layouts = column(slider, x_dropdown, y_dropdown, region_selection )
    layout = row(widget_layouts, plot)
    return layout
