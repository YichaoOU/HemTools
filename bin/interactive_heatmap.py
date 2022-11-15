#!/usr/bin/env python

import pandas as pd
import sys
import os
import argparse
import math
import os
import altair as alt
import pandas as pd
import numpy as np
import yaml
import glob
from yaml import Loader, Dumper
def generic_df_reader(args):
	if "npz" == args.input.split(".")[-1]:
		npz = np.load('result.npz')
		df = pd.DataFrame(npz['matrix'])
		df.columns = npz['labels']
		return df
	if args.sep=="auto":
		args.sep = guess_sep(args.input)
	if args.header:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0)
		else:
			df = pd.read_csv(args.input,sep=args.sep)
	else:
		if args.index:
			df = pd.read_csv(args.input,sep=args.sep,index_col=0,header=None)
		else:
			df = pd.read_csv(args.input,sep=args.sep,header=None)
	return df
def guess_sep(x):
	with open(x) as f:
		for line in f:
			tmp1 = len(line.strip().split(","))
			tmp2 = len(line.strip().split("\t"))
			# print (tmp1,tmp2)
			if tmp1 > tmp2:
				return ","
			if tmp2 > tmp1: 
				return "\t"
			else:
				print ("Can't determine the separator. Please input manually")
				exit()
				
def zoom_bar(data, zoom_bar_color_by, zoom_bar_title,zoom_width,zoom_bar_x_col,zoom_bar_x_order,color_min_v,color_max_v):
	"""Create one layer heatmap for zoom bar.
	Parameters
	----------
	data :pandas.DataFrame
		Data frame with site and metric value.
	zoom_bar_color_by : str
		Column in `data` with values to color by.
	title : str
		Title of the plot.
	Returns
	-------
	altair.Chart
	"""
	zoom_brush = alt.selection_interval(encodings=['x'], mark=alt.BrushConfig(stroke='black',strokeWidth=2))
	zoom = (alt.Chart(data)
			.mark_rect()
			.encode(x=alt.X(f'{zoom_bar_x_col}:O',
						   sort=zoom_bar_x_order),
					color=alt.Color(zoom_bar_color_by, 
									 scale=alt.Scale(scheme='greys',  
													 domain=[color_min_v,color_max_v]),
									legend=alt.Legend(orient='left',
													 labelFontSize=15,
													 titleFontSize=16,
													 title=zoom_bar_title)))
			.add_selection(zoom_brush)
			.properties(width=zoom_width,
						title='zoom bar'))
	return zoom,zoom_brush
def DMS_heatmaps(data,tooltips,heatmap_color_by,heatmap_x_col,heatmap_x_order,heatmap_y_col,heatmap_y_order,color_min_v,color_max_v,heatmap_star_annotation_col,heatmap_height,zoom_brush):
	"""Create main heatmap for one condition.
	The heatmap is the results of three layers.
	*heatmap* is the main DMS data
	*wildtype* marks wildtype data with an 'x'
	*nulls* creates grey cells for missing data.
	If you exclude nulls, missing data is white, 
	which is appropriate for some color schemes
	but not all.
	Parameters
	----------
	data :pandas.DataFrame
		Main dataframe
	heatmap_color_by : str
		Column in `data` with values to color by.
	tooltips : list
		Column values to show when mouse hover
	Returns
	-------
	altair.Chart
	"""
	cell_selector = alt.selection_single(on='mouseover',empty='none')
	# zoom_brush = alt.selection_interval(encodings=['x'], mark=alt.BrushConfig(stroke='black',strokeWidth=2))
	# tmp = data.sort_values("pos2")
	# tmp = tmp.drop_duplicates("pos")
	# pos_oder = tmp.pos.tolist()
	# tooltips = ['mutation','log2FoldChange','pvalue','padj']
	# everything is site v mutant
	base = (alt.Chart(data)
			.encode(x=alt.X(f'{heatmap_x_col}:O',
							 sort=heatmap_x_order,
							 axis=alt.Axis(titleFontSize=15)),
					y=alt.Y(f'{heatmap_y_col}:O',
							 sort=heatmap_y_order,
							axis=alt.Axis(labelFontSize=12,
										  titleFontSize=15))
				   )
		   )
	heatmap = (base
			   .mark_rect()
			   .encode(color=alt.Color(heatmap_color_by,
									   type='quantitative', 
									   scale=alt.Scale(range=["#0505ff",'#afecfa', "#fafafa","#fff6c2", "#fc0303"],
													   type="linear",
													   exponent=4,
													   domain=[color_min_v,
															   color_max_v],
													   ),
									   legend=alt.Legend(orient='left',
														gradientLength=100)),
					   stroke=alt.value('black'),
					   strokeWidth=alt.condition(cell_selector,
												 alt.value(2),
												 alt.value(0)),
					   tooltip=tooltips
					  )
			  )
	
	text = base.mark_text(color='black').encode(
		text=f'{heatmap_star_annotation_col}:N'
		)
	nulls = (base
			 .mark_rect()
			 .transform_filter(f"!isValid(datum.{heatmap_color_by})")
			 .mark_rect(opacity=0.5)
			 .encode(alt.Color(f'{heatmap_color_by}:N',
							   scale=alt.Scale(scheme='greys'),
							   legend=None)
					)
			)
	
	return ((heatmap + nulls +text)
			.interactive()
			.add_selection(cell_selector)  # mouse over highlighting
			.transform_filter(zoom_brush)  # add zoom bar filtering
			.properties(height=heatmap_height, title=' '.join(heatmap_color_by.split('_'))))
def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-f',"--input",  help="data table to be plot",required=True)
	mainParser.add_argument('-o',"--output",  help="output visualization html file",required=True)
	mainParser.add_argument("--reformat_config",  help="reformat data table",default=None)
	mainParser.add_argument('--header',  help="data table has header", action='store_true')
	mainParser.add_argument('--index',  help="data table has index", action='store_true')
	mainParser.add_argument('--sep',  help="data table separator", default="auto")

	# mainParser.add_argument('-s',"--sample_list",  help="table rows, a list of samples, these are supposed to be folder names, one column",required=True)
	# mainParser.add_argument('-f','--feature_list',  help="table columns, map file name to specific feature name",required=True)
	# mainParser.add_argument('--softlinks',  help=argparse.SUPPRESS,default="")
	# mainParser.add_argument('--treatment_bam',  help=argparse.SUPPRESS)
	# mainParser.add_argument('--port',  help=argparse.SUPPRESS)

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args

def parse_file_kasey(f):
    df = pd.read_csv(f,sep="\t")
    df['pos'] = [x[:-1] for  x in df.mutation]
    df['pos2'] = [int(x[1:-1]) for  x in df.mutation]
    df['mutant'] = [x[-1] for x in df.mutation]
    df['sig'] = df.apply(lambda r:abs(r.log2FoldChange)>1 and r.BF,axis=1)
    df['BF'] = df.BF.map({True:"*",False:""})
    df.sig = df.pos.map(df.groupby("pos")['sig'].sum().to_dict())
    return df

def get_plot_parameters(f):
	if not os.path.isfile(f):
		print (f"{f} not exist")
		exit()
	return yaml.load(open(f),Loader=Loader)

args = my_args()
if args.reformat_config == "kasey":
    df = parse_file_kasey(args.input)
    args.reformat_config = "/home/yli11/HemTools/share/misc/interactive_heatmap.kasey.yaml"
else:
    df = generic_df_reader(args)

# plot parameters and pre-process some variables, such as x-order
plot_parameters = get_plot_parameters(args.reformat_config)
# print (plot_parameters)
globals().update(plot_parameters)
# print(globals())
# print (tooltips)
tooltips = tooltips.split(",")
zoom_bar_x_order,ascending = zoom_bar_x_order.split(",")
zoom_bar_x_order = df.sort_values(zoom_bar_x_order,ascending=int(ascending)).drop_duplicates(zoom_bar_x_col)[zoom_bar_x_col].tolist()

heatmap_x_order,ascending = heatmap_x_order.split(",")
heatmap_x_order = df.sort_values(heatmap_x_order,ascending=int(ascending)).drop_duplicates(heatmap_x_col)[heatmap_x_col].tolist()

heatmap_y_order,ascending = heatmap_y_order.split(",")
heatmap_y_order = df.sort_values(heatmap_y_order,ascending=int(ascending)).drop_duplicates(heatmap_y_col)[heatmap_y_col].tolist()

if heatmap_star_annotation_col=="":
    df['empty'] = ""
    heatmap_star_annotation_col = "empty"


# main functions
zoom,zoom_brush = zoom_bar(df, zoom_bar_color_by, zoom_bar_title,zoom_width,zoom_bar_x_col,zoom_bar_x_order,zoom_bar_color_min_v,zoom_bar_color_max_v)
expression = DMS_heatmaps(df, tooltips,heatmap_color_by,heatmap_x_col,heatmap_x_order,heatmap_y_col,heatmap_y_order,heatmap_color_min_v,heatmap_color_max_v,heatmap_star_annotation_col,heatmap_height,zoom_brush)

# save chart
chart = (alt.vconcat(zoom, expression, spacing=0)
         .configure_title(anchor='start',
                          fontSize=20))
chart.save(args.output)














