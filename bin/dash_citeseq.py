
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objs as go
import dash_table
import plotly_express as px
# from  glasbey import Glasbey
from dash.dependencies import Input, Output, State
import re
import os
import base64
import io 
import numpy as np
# from cairosvg import svg2png
import joypy
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import cm
import datetime
import getpass
import argparse
import os


# exec(open("dash_main.py").read())

external_stylesheets = [dbc.themes.BOOTSTRAP]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

prefix = "sc_integration_yli11_2021-04-10"


def read_pkl(f):
	df = pd.read_pickle(f).T
	df.index = [x.upper() for x in df.index.tolist()]
	return df


df = pd.read_csv("%s_Harmony_UMAP.csv"%(prefix))
df.index = df.barcodekey.tolist()
rna_df = read_pkl("%s.rna.log_norm.pkl"%(prefix))
antibody_df = read_pkl("%s.antibody.log_norm.pkl"%(prefix))
antibody_df = antibody_df.transform(lambda x:np.log2(x+1))
antibody_list = antibody_df.index.tolist()



def get_exp_gene(g):
	g = g.upper()
	try:
		return rna_df.loc[g]
	except:
		return 1
	

gene_input = html.Div(
	[

			dbc.Label('Input a Gene Name to highlight the plots below'),
			dbc.Input(id="gene_search", type="text",value="GATA1", style={'width': '50%'},),
			html.P(id='output'),

	]		
)


antibody_selection = html.Div(
	[
		# dbc.Row(
			dbc.Label('Select two antibodies to display'),
			dbc.Checklist(
				options=[{"label": i, "value": i} for i in antibody_list],
				id="antibody_selection",
				value=[antibody_list[0], antibody_list[1]],
				labelStyle={'display': 'inline-block'},
			),
		# ),
	]		
)

app.layout = dbc.Container(
	[
		html.H2("scRNA-seq data visualization (cite-seq version)"),
		html.Hr(style={"margin-bottom":"0px"}),
		dbc.Row( # select gene and antibody
			[
				dbc.Col(gene_input, md=5),
				dbc.Col(antibody_selection, md=7),

			],
			align="top",
		),

		

		dbc.Row( # scatter plot, plotly
			[
				dbc.Col(dcc.Graph(id="antibody_scatter", style={"display": "inline-block",'width': '900px', 'height': '900px'}), md=6),
				dbc.Col(dcc.Graph(id="UMAP_scatter", style={"display": "inline-block",'width': '900px', 'height': '900px'}), md=6),

			],
			align="top",
		),	
		dbc.Row( # ridge plot, joypy
			[
				html.Div(id='ridge_plot',children=[]),

			],
			align="top",
		),				
	],
	fluid=True,
)


@app.callback(
	Output("output", "children"),
	[
	Input('gene_search', 'n_submit'),
	Input('gene_search', 'n_blur')
	],
	[
	State('gene_search', 'value')
	]	
	)
def update_output(ns,nb,g):
	try:
		selected_gene = rna_df.loc[g.upper()]
	except:
		return u'''%s not found'''%(g)
	return ""	


@app.callback(
	Output("antibody_scatter", "figure"),
	[
	Input('gene_search', 'n_submit'),
	Input('gene_search', 'n_blur'),
	Input('antibody_selection', 'value')
	],
	[
	State('gene_search', 'value')
	]	
	)
def make_figure_antibody(ns,nb,antibody_selection,g):

	
	tmp = df.copy()
	tmp['gene_exp'] = get_exp_gene(g)
	AB1 = antibody_selection[0]
	AB2 = antibody_selection[1]
	tmp[AB1] = antibody_df.loc[AB1]
	tmp[AB2] = antibody_df.loc[AB2]

	fig2 = px.scatter(tmp,x=AB1,y=AB2,color='gene_exp',symbol="Channel",hover_data=['barcodekey','n_genes','n_counts','louvain_labels'],opacity=0.5,size_max=3,template="simple_white")
	fig2.update_layout(coloraxis_colorbar=dict(yanchor="top", y=0.5, x=1,ticks="outside",len=0.5))
	return fig2

@app.callback(
	Output("UMAP_scatter", "figure"),
	[
	Input('gene_search', 'n_submit'),
	Input('gene_search', 'n_blur')
	],
	[
	State('gene_search', 'value')
	]	
	)
def make_figure_UMAP(ns,nb,g):

	tmp = df.copy()
	tmp['gene_exp'] = get_exp_gene(g)
	fig2 = px.scatter(tmp,x="UMAP1",y="UMAP2",color='gene_exp',symbol="Channel",hover_data=['barcodekey','n_genes','n_counts','louvain_labels'],opacity=0.5,size_max=3,template="simple_white")
	fig2.update_layout(coloraxis_colorbar=dict(yanchor="top", y=0.5, x=1,ticks="outside",len=0.5))
	return fig2

@app.callback(
	Output("ridge_plot", "children"),
	[
	Input('gene_search', 'n_submit'),
	Input('gene_search', 'n_blur')
	],
	[
	State('gene_search', 'value')
	]	
	)
def make_joyplot(ns,nb,g):
	tmp = df.copy()
	tmp['gene_exp'] = get_exp_gene(g)
	joypy.joyplot(tmp, by="Channel", ylim='own',column="gene_exp")
	plt.savefig("test.png",bbox_inches='tight')
	s2 = base64.b64encode(open("test.png","rb").read()).decode("utf-8").replace("\n", "")
	return [html.Img(id="plot",src="data:image/png;base64,%s"%(s2))]



if __name__ == '__main__':
	app.run_server(debug=False,host='0.0.0.0',port=8079)

