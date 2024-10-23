import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib as mpl
import matplotlib.pyplot as plt

from utils_config import mapper_methods


LINEWIDTH = 3



def plot_barplot(df_performance, metric, n_top=5, sort_by='Average', cmap='Greens', ax=None, rdm=None):
    df_plot = df_performance[(df_performance['Metric']==metric)
                            & (~df_performance['Group'].isin(['full_data', 'Average', 'WeightedAverage']))]
    
    if n_top is not None:
        top_methods = df_performance[(df_performance['Metric']==metric)
                            & (df_performance['Group']==sort_by)]
        top_methods = top_methods.sort_values('Value', ascending=metric=='Rank')
        top_methods = top_methods.head(n_top)['Method'].tolist()
        df_plot = df_plot[df_plot['Method'].isin(top_methods)]
    
    m_props = {'markerfacecolor': 'white', 'markeredgecolor': 'black', 'markersize': '20'}
    plot = sb.barplot(data=df_plot, y='Value', x='Method', 
                      order=top_methods if n_top is not None else None,
                      palette=cmap,
                      errwidth=LINEWIDTH,
                      capsize=0.5,
                      ax=ax)
                      
    plot = sb.stripplot(data=df_plot, y='Value', x='Method', 
                      order=top_methods if n_top is not None else None,
                      color='gray',
                      size=2,
                      ax=ax)

    xlabels = plot.get_xticklabels()
    xlabels = [mapper_methods[el.get_text().split('_')[0]] for el in xlabels]
    plot.set_xticklabels(xlabels, rotation=90)
    
    sb.despine(ax=plot)
    plot.grid(False)
    plot.set_ylabel(metric, labelpad=2)
    plot.set_xlabel(None)
    plot.tick_params(axis='both', pad=0)
    
    plot.spines['left'].set_linewidth(LINEWIDTH)
    plot.spines['bottom'].set_linewidth(LINEWIDTH) 

    if rdm is not None:
        ax.axhline(y=rdm, color='gray', linestyle='--')


def plot_boxplot(df_performance, metric, n_top=5, sort_by='Average', cmap='Greens', ax=None, rdm=None):
    df_plot = df_performance[(df_performance['Metric']==metric)
                            & (~df_performance['Group'].isin(['full_data', 'Average', 'WeightedAverage']))]
    
    if n_top is not None:
        top_methods = df_performance[(df_performance['Metric']==metric)
                            & (df_performance['Group']==sort_by)]
        top_methods = top_methods.sort_values('Value', ascending=metric=='Rank')
        top_methods = top_methods.head(n_top)['Method'].tolist()
        df_plot = df_plot[df_plot['Method'].isin(top_methods)]
    
    m_props = {'markerfacecolor': 'white', 'markeredgecolor': 'black', 'markersize': '5'}
    plot = sb.boxplot(data=df_plot, y='Value', x='Method', 
                      order=top_methods if n_top is not None else None,
                      palette=cmap, showmeans=True, 
                      meanprops=m_props, 
                      capprops = {"linewidth": LINEWIDTH},
                      flierprops={'markersize': 3},
                      medianprops = {'linewidth': LINEWIDTH},
                      boxprops={"linewidth": LINEWIDTH},
                      whiskerprops = {"linewidth": LINEWIDTH},
                      ax=ax)

    xlabels = plot.get_xticklabels()
    xlabels = [mapper_methods[el.get_text().split('_')[0]] for el in xlabels]
    plot.set_xticklabels(xlabels, rotation=90)
    
    sb.despine(ax=plot)
    plot.grid(False)
    plot.set_ylabel(metric, labelpad=2)
    plot.set_xlabel(None)
    plot.tick_params(axis='both', pad=0)
    
    plot.spines['left'].set_linewidth(LINEWIDTH)
    plot.spines['bottom'].set_linewidth(LINEWIDTH)

    if rdm is not None:
        ax.axhline(y=rdm, color='gray', linestyle='--')
