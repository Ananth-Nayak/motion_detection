from scripts import df
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import column,row
from bokeh.models import ColumnDataSource, HoverTool

df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds =ColumnDataSource(df)

p = figure(x_axis_type = 'datetime', height = 200,width =1500,title = 'Motion Grapgh')
p.yaxis.minor_tick_line_color = None
p.xaxis.minor_tick_line_color = None
p.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips =[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

q = p.quad(left = "Start",right = "End",bottom = 0,top = 1,color = "green",source = cds)
layout = row(p,sizing_mode="scale_width")
output_file("Graph.html")
show(layout)