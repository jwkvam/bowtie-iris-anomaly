#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie import cache
from bowtie.control import DropDown, Slider
from bowtie.control import Button, Switch, Number

from bowtie.visual import Plotly

import numpy as np
import pandas as pd
import plotlywrapper as pw

from sklearn import manifold
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler

iris = pd.read_csv('./iris.csv')
iris = iris.drop(iris.columns[0], axis=1)

attrs = iris.columns[:-1]

species = iris.Species.unique()

algos = ['MDS', 'TSNE', 'Locally Linear Embedding']

algo_select = DropDown(caption='Manifold Algorithm', labels=algos, values=algos)
species_select = DropDown(caption='Species', labels=species, values=species, multi=True)
normalize_switch = Switch(caption='Normalize')
random_seed = Number(caption='Seed', start=0, minimum=0, step=1)
neighbor_slider = Slider(caption='Neighbors', start=1, minimum=1, maximum=20, step=1)
perplex_slider = Slider(caption='Perplexity', start=30, minimum=1, maximum=200, step=1)

replot_button = Button(label='Replot')

anomplot = Plotly()
attrplot = Plotly()


def get_species_data(species, normalize):
    species = [s['value'] for s in species]
    data = iris.query('Species in @species').iloc[:, :-1]
    if normalize:
        mms = MinMaxScaler()
        data.iloc[:] = mms.fit_transform(data)
    return data


def baseviz(algo, normalize, neighbors, species, perplex):
    # attr_data = get_species_data(species, normalize).iloc[:, :4]
    if (algo is None or
            normalize is None or
            species is None):
        return
    baseviz2(algo, normalize, neighbors, species, perplex)

def replot():
    algo = algo_select.get()
    neighbors = neighbor_slider.get()
    normalize = normalize_switch.get()
    species = species_select.get()
    perplex = perplex_slider.get()
    baseviz2(algo, normalize, neighbors, species, perplex)

def baseviz2(algo, normalize, neighbors, species, perplex):
    algo = algo['label']
    attr_data = get_species_data(species, normalize)

    anomplot.progress.do_percent(0)
    anomplot.progress.do_visible(True)


    seed = random_seed.get()
    if algo == 'TSNE':
        mnf = manifold.TSNE(random_state=seed, perplexity=perplex)
    elif algo == 'MDS':
        mnf = manifold.MDS(random_state=seed)
    elif algo == 'Locally Linear Embedding':
        mnf = manifold.LocallyLinearEmbedding(random_state=seed)
    else:
        print(algo)

    anomplot.progress.do_inc(2)

    reduced = mnf.fit_transform(attr_data)

    anomplot.progress.do_inc(5)

    nn = NearestNeighbors(neighbors)
    nn.fit(reduced)

    anomplot.progress.do_inc(3)

    dists = nn.kneighbors()[0][:, -1]

    msize = 60 * dists / max(dists)

    chart = pw.Chart()
    for i, (x, y) in enumerate(reduced):
        if i == nth:
            chart += pw.scatter(x, y, markersize=msize[i], color='red')
        else:
            chart += pw.scatter(x, y, markersize=msize[i], color='blue', opacity=0.5)
        anomplot.progress.do_inc(1)
    chart.legend(False)
    chart.layout['hovermode'] = 'closest'
    anomplot.progress.do_visible(False)
    cache.save('anomaly', chart.dict)
    anomplot.do_all(chart.dict)

    chart = attr_data.T.plotly.line(opacity=0.5)
    chart.legend(False)
    chart.layout['hovermode'] = 'closest'
    attrplot.do_all(chart.dict)


def anom_click_point(point):
    nth = point['curve']
    normalize = normalize_switch.get()
    species = species_select.get()

    attr_data = get_species_data(species, normalize)

    pix = attr_data.index[nth]

    chart = pw.Chart()
    for i, (idx, row) in enumerate(attr_data.iterrows()):
        if i == nth:
            chart += row.plotly.line(width=10)
        else:
            chart += row.plotly.line(opacity=0.5)
    chart.legend(False)
    chart.layout['hovermode'] = 'closest'
    attrplot.do_all(chart.dict)


def anom_select_points(points):
    print(points)


def attr_click_point(point):
    nth = point['curve']
    algo = algo_select.get()
    neighbors = neighbor_slider.get()
    normalize = normalize_switch.get()
    species = species_select.get()
    perplex = perplex_slider.get()
    data = cache.load('anomaly')

    chart = pw.Chart(data=data['data'], layout=data['layout'])

    chart.data[nth]['line']['color'] = 'red'
    chart.data[nth]['opacity'] = 1

    anomplot.do_all(chart.dict)


def attr_select_points(points):
    print(points)


from bowtie import command

@command
def construct():
    from bowtie import Layout
    description = """
Iris Anomalies
==============

"""
    layout = Layout(description=description, title='Iris Anomaly', background_color='LavenderBlush', debug=False)
    layout.add_visual(anomplot)
    layout.add_visual(attrplot, next_row=True)

    layout.add_controller(algo_select)
    layout.add_controller(species_select)
    layout.add_controller(normalize_switch)
    layout.add_controller(random_seed)
    layout.add_controller(neighbor_slider)
    layout.add_controller(perplex_slider)
    layout.add_controller(replot_button)

    layout.subscribe(baseviz,
                     algo_select.on_change,
                     normalize_switch.on_switch,
                     neighbor_slider.on_change,
                     species_select.on_change,
                     perplex_slider.on_change)

    layout.subscribe(replot, replot_button.on_click)

    layout.subscribe(anom_click_point, anomplot.on_click)
    layout.subscribe(anom_click_point, anomplot.on_hover)
    layout.subscribe(anom_select_points, anomplot.on_select)

    layout.subscribe(attr_click_point, attrplot.on_click)
    layout.subscribe(attr_click_point, attrplot.on_hover)
    layout.subscribe(attr_select_points, attrplot.on_select)

    layout.build()
