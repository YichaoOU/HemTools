#!/usr/bin/env python

import warnings
warnings.filterwarnings('ignore') # supress warnings due to some future deprications

import pandas as pd
import sys
import matplotlib
matplotlib.use('agg')
import os
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import argparse
import datetime
import getpass
import uuid
from scipy.interpolate import interp1d
import re, string
# from matplotlib_venn import venn2
import subprocess
import pandas as pd
import seaborn as sns
# %matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import numpy as np
from matplotlib.colors import ListedColormap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import pandas as pd
import numpy as np
import networkx as nx
# import igraph as ig

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn import preprocessing, feature_extraction, model_selection
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from itertools import count

import random

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import stellargraph as sg
from stellargraph.data import EdgeSplitter
from stellargraph.mapper import GraphSAGELinkGenerator, GraphSAGENodeGenerator
from stellargraph.layer import GraphSAGE, link_classification
from stellargraph.data import UniformRandomWalk
from stellargraph.data import UnsupervisedSampler
from sklearn.model_selection import train_test_split

from tensorflow import keras

from stellargraph import globalvar
import pandas as pd
import numpy as np
import random
import networkx as nx
from sklearn.cluster import DBSCAN
from functools import reduce
import matplotlib.pyplot as plt

import sys
# exec(open("main_filter.py").read())

import glob


def load_features(input_data):
    # Summarise features by terrorist group
    dt_collect = input_data[
        ["eventid", "nperps", "success", "suicide", "nkill", "nwound", "gname"]
    ]
    dt_collect.fillna(0, inplace=True)
    dt_collect.nperps[dt_collect.nperps < 0] = 0

    summarize_by_gname = (
        dt_collect.groupby("gname")
        .agg(
            {
                "eventid": "count",
                "nperps": "sum",
                "nkill": "sum",
                "nwound": "sum",
                "success": "sum",
            }
        )
        .reset_index()
    )
    summarize_by_gname.columns = [
        "gname",
        "n_attacks",
        "n_nperp",
        "n_nkil",
        "n_nwound",
        "n_success",
    ]
    summarize_by_gname["success_ratio"] = (
        summarize_by_gname["n_success"] / summarize_by_gname["n_attacks"]
    )
    summarize_by_gname.drop(["n_success"], axis=1, inplace=True)

    # Collect counts of each attack type
    dt_collect = input_data[["gname", "attacktype1_txt"]]
    gname_attacktypes = (
        dt_collect.groupby(["gname", "attacktype1_txt"])["attacktype1_txt"]
        .count()
        .to_frame()
    )
    gname_attacktypes.columns = ["attacktype_count"]
    gname_attacktypes.reset_index(inplace=True)
    gname_attacktypes_wide = gname_attacktypes.pivot(
        index="gname", columns="attacktype1_txt", values="attacktype_count"
    )
    gname_attacktypes_wide.fillna(0, inplace=True)
    gname_attacktypes_wide.drop(["Unknown"], axis=1, inplace=True)

    # Collect counts of each target type
    dt_collect = input_data[["gname", "targtype1_txt"]]
    gname_targtypes = (
        dt_collect.groupby(["gname", "targtype1_txt"])["targtype1_txt"]
        .count()
        .to_frame()
    )
    gname_targtypes.columns = ["targtype_count"]
    gname_targtypes.reset_index(inplace=True)
    gname_targtypes_wide = gname_targtypes.pivot(
        index="gname", columns="targtype1_txt", values="targtype_count"
    )
    gname_targtypes_wide.fillna(0, inplace=True)
    gname_targtypes_wide.drop(["Unknown"], axis=1, inplace=True)

    # Combine all features
    data_frames = [summarize_by_gname, gname_attacktypes_wide, gname_targtypes_wide]
    gnames_features = reduce(
        lambda left, right: pd.merge(left, right, on=["gname"], how="outer"),
        data_frames,
    )
    return gnames_features


def load_network(input_data):
    # Create country_decade feature
    dt_collect = input_data[["eventid", "country_txt", "iyear", "gname"]]
    dt_collect["decade"] = (dt_collect["iyear"] // 10) * 10
    dt_collect["country_decade"] = (
        dt_collect["country_txt"] + "_" + dt_collect["decade"].map(str) + "s"
    )
    dt_collect = dt_collect[dt_collect.gname != "Unknown"]

    # Create a country_decade edgelist
    gnames_country_decade = (
        dt_collect.groupby(["gname", "country_decade"])
        .agg({"eventid": "count"})
        .reset_index()
    )
    gnames_country_decade_edgelist = pd.merge(
        gnames_country_decade, gnames_country_decade, on="country_decade", how="left"
    )
    gnames_country_decade_edgelist.drop(
        ["eventid_x", "eventid_y"], axis=1, inplace=True
    )
    gnames_country_decade_edgelist.columns = ["source", "country_decade", "target"]
    gnames_country_decade_edgelist = gnames_country_decade_edgelist[
        gnames_country_decade_edgelist.source != gnames_country_decade_edgelist.target
    ]

    G_country_decade = nx.from_pandas_edgelist(
        gnames_country_decade_edgelist, source="source", target="target"
    )

    # Create edgelist from the related column
    dt_collect = input_data["related"]
    dt_collect.dropna(inplace=True)
    gname_event_mapping = input_data[["eventid", "gname"]].drop_duplicates()
    gname_event_mapping.eventid = gname_event_mapping.eventid.astype(str)

    G_related = nx.parse_adjlist(
        dt_collect.values, delimiter=", "
    )  # attacks that are related
    df_related = nx.to_pandas_edgelist(G_related)
    df_related.replace(" ", "", regex=True, inplace=True)
    df_source_gname = pd.merge(
        df_related,
        gname_event_mapping,
        how="left",
        left_on="source",
        right_on="eventid",
    )
    df_source_gname.rename(columns={"gname": "gname_source"}, inplace=True)
    df_target_gname = pd.merge(
        df_source_gname,
        gname_event_mapping,
        how="left",
        left_on="target",
        right_on="eventid",
    )
    df_target_gname.rename(columns={"gname": "gname_target"}, inplace=True)

    # Filtering and cleaning
    gnames_relations_edgelist = df_target_gname[
        df_target_gname.gname_source != df_target_gname.gname_target
    ]
    gnames_relations_edgelist = gnames_relations_edgelist[
        gnames_relations_edgelist.gname_source != "Unknown"
    ]
    gnames_relations_edgelist = gnames_relations_edgelist[
        gnames_relations_edgelist.gname_target != "Unknown"
    ]
    gnames_relations_edgelist = gnames_relations_edgelist[
        ["gname_source", "gname_target"]
    ]
    gnames_relations_edgelist.dropna(inplace=True)

    G_rel = nx.from_pandas_edgelist(
        gnames_relations_edgelist, source="gname_source", target="gname_target"
    )

    # Merging two graphs
    G = nx.compose(G_country_decade, G_rel)

    return G


def dbscan_hyperparameters(embeddings, e_lower=0.3, e_upper=0.8, m_lower=3, m_upper=15):
    """
    function to run dbscan clustering greedily for different min_samples and e_eps and discover number of resulting clusters and noise points
    """
    n_clusters_res = []
    n_noise_res = []
    e_res = []
    m_res = []

    for e in np.arange(e_lower, e_upper, 0.1):
        print("eps:" + str(e))
        for m in np.arange(m_lower, m_upper, 1):
            db = DBSCAN(eps=e, min_samples=m).fit(embeddings)
            labels = db.labels_
            n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise_ = list(labels).count(-1)
            n_clusters_res.append(n_clusters_)
            n_noise_res.append(n_noise_)
            e_res.append(e)
            m_res.append(m)

    plt.plot(n_clusters_res, n_noise_res, "ro")
    plt.xlabel("Number of clusters")
    plt.ylabel("Number of noise points")
    plt.show()

    dt = pd.DataFrame(
        {
            "n_clusters": n_clusters_res,
            "n_noise": n_noise_res,
            "eps": e_res,
            "min_samples": m_res,
        }
    )

    return dt


def cluster_external_internal_edges(G, cluster_df, cluster_name="cluster"):
    nclusters = pd.unique(cluster_df[cluster_name])

    nexternal_edges = []
    ninternal_edges = []
    for cl in nclusters:
        nodes_in_cluster = list(cluster_df.index[cluster_df[cluster_name] == cl].values)
        external = list(nx.edge_boundary(G, nodes_in_cluster))
        nexternal_edges.append(len(external))
        internal = G.subgraph(nodes_in_cluster)
        ninternal_edges.append(len(internal.edges()))
    df = pd.DataFrame(
        {
            "cluster": nclusters,
            "nexternal_edges": nexternal_edges,
            "ninternal_edges": ninternal_edges,
        }
    )
    df["ratio"] = df["ninternal_edges"] / df["nexternal_edges"]
    return df


count_file = sys.argv[1]
file = sys.argv[2]
label_user = sys.argv[3]
df = pd.read_csv(file,sep="\t")
counts = pd.read_csv(count_file,index_col=0)
print ("count table size",counts.shape)


myList = [9606,10090]
df2 = df.copy()
df = df2.copy()
df = df[df['Organism ID Interactor A'].isin(myList)]
df = df[df['Organism ID Interactor B'].isin(myList)]
df['Official Symbol Interactor A'] = df['Official Symbol Interactor A'].str.upper()
df['Official Symbol Interactor B'] = df['Official Symbol Interactor B'].str.upper()
df = df[['Official Symbol Interactor A','Official Symbol Interactor B']]
df = df.dropna()
gene_list = df['Official Symbol Interactor A'].tolist()+df['Official Symbol Interactor B'].tolist()


gene_list = set(gene_list).intersection(counts.index)
gene_list = list(set(gene_list))

df = df[df['Official Symbol Interactor A'].isin(gene_list)]
df = df[df['Official Symbol Interactor B'].isin(gene_list)]

gene_list = df['Official Symbol Interactor A'].tolist()+df['Official Symbol Interactor B'].tolist()
gene_list = list(set(gene_list))
G=nx.from_pandas_edgelist(df, 'Official Symbol Interactor A', 'Official Symbol Interactor B')
print(nx.info(G))

nx.write_gml(G, "filtered_network_1019.gml")



filtered_features = counts.loc[gene_list]

node_features = filtered_features.transform(lambda x: np.log1p(x))
node_features = node_features[~node_features.index.duplicated(keep='first')]

Gs = sg.StellarGraph.from_networkx(G, node_features=node_features)
print(Gs.info())
number_of_walks = 3
length = 2
batch_size = 50
epochs = 20
num_samples = [10, 10]
layer_sizes = [15, 15]
learning_rate = 2e-2
# number_of_walks = 1
# length = 2
# batch_size = 50
# epochs = 1
# num_samples = [3, 3]
# layer_sizes = [5, 5]
# learning_rate = 1e-1
unsupervisedSamples = UnsupervisedSampler(
    Gs, nodes=G.nodes(), length=length, number_of_walks=number_of_walks
)
generator = GraphSAGELinkGenerator(Gs, batch_size, num_samples)
train_gen = generator.flow(unsupervisedSamples)
assert len(layer_sizes) == len(num_samples)
graphsage = GraphSAGE(
    layer_sizes=layer_sizes, generator=generator, bias=True, dropout=0.0, normalize="l2"
)
x_inp, x_out = graphsage.in_out_tensors()
prediction = link_classification(
    output_dim=1, output_act="sigmoid", edge_embedding_method="ip"
)(x_out)
model = keras.Model(inputs=x_inp, outputs=prediction)
model.compile(
    optimizer=keras.optimizers.Adam(lr=learning_rate),
    loss=keras.losses.binary_crossentropy,
    metrics=[keras.metrics.binary_accuracy],
)
import time

class TimeHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.times = []

    def on_epoch_begin(self, epoch, logs={}):
        self.epoch_time_start = time.time()

    def on_epoch_end(self, epoch, logs={}):
        self.times.append(time.time() - self.epoch_time_start)

time_callback = TimeHistory()

history = model.fit(
    train_gen,
    epochs=epochs,
    verbose=2,
    use_multiprocessing=False,
    workers=1,
    shuffle=True,

)

node_ids = list(Gs.nodes())
node_gen = GraphSAGENodeGenerator(Gs, batch_size, num_samples).flow(node_ids)
embedding_model = keras.Model(inputs=x_inp[::2], outputs=x_out[0])

node_embeddings = embedding_model.predict(node_gen, workers=1, verbose=1)
node_embeddings.shape
X = node_embeddings
emb_df = pd.DataFrame(node_embeddings,index=node_ids)
emb_df.to_csv("%s_GraphSAGE.node_emb.csv"%(label_user))

transform = TSNE  # PCA
trans = transform(n_components=2, random_state=0)
emb_transformed = pd.DataFrame(trans.fit_transform(X), index=node_ids)

alpha = 0.7
fig, ax = plt.subplots(figsize=(7, 7))
myList = ['SPI1','NFIX']
ax.scatter(emb_transformed[0], emb_transformed[1], alpha=alpha)
ax.scatter(emb_transformed.loc[myList][0], emb_transformed.loc[myList][1], alpha=1,color="red")
ax.set(aspect="equal", xlabel="$X_1$", ylabel="$X_2$")
plt.title("{} visualization of GraphSAGE embeddings".format(transform.__name__))
plt.savefig("%s_overall_clustering.png"%(label_user))

emb_transformed.to_csv("%s_GraphSAGE.emb_tsne.csv"%(label_user))
db_dt = utils.dbscan_hyperparameters(
    node_embeddings, e_lower=0.1, e_upper=0.9, m_lower=5, m_upper=15
)
db_dt.to_csv("%s_db_dt.csv"%(label_user))
db = DBSCAN(eps=0.1, min_samples=5).fit(node_embeddings)


clustered_df = pd.DataFrame(node_embeddings, index=node_ids)
clustered_df["cluster"] = db.labels_
clustered_df.groupby("cluster").count()[0].sort_values(ascending=False)[0:15]
cluster_id=1
sub_nodelist = list(clustered_df.index[clustered_df.cluster == cluster_id])
sub_edgelist = G.edges(sub_nodelist)
cluster_G = G.edge_subgraph(sub_edgelist)



unfrozen_graph = nx.Graph(cluster_G)
# unfrozen_graph.remove_nodes_from(list(nx.isolates(unfrozen_graph)))
print(nx.info(unfrozen_graph))
pos = nx.fruchterman_reingold_layout(unfrozen_graph, seed=123, iterations=30)

plt.figure(figsize=(10, 8))
nx.draw_networkx(unfrozen_graph, pos, edge_color="#26282b", node_color="blue", alpha=0.3)
plt.axis("off")
plt.savefig("%s_test.network.png"%(label_user))



