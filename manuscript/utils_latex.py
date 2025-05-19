import pandas as pd
import numpy as np


from utils_config import mapper_methods


def to_print_df(df_performance, metrics, n_top=3, grouping='Epitope'):
    cat_models = ['MixTCRpred', 'NetTCR-Cat', 'TCRGP']
    df_tmp = df_performance[df_performance['Metric'].isin(metrics)]
    df_tmp = df_tmp[~df_tmp['Group'].isin(['WeightedAverage', 'Average', 'full_data'])]
    df_mean = df_tmp.groupby(['BaseModel', 'Metric'])['Value'].mean().unstack()[metrics]
    df_std = df_tmp.groupby(['BaseModel', 'Metric'])['Value'].std().unstack()[metrics]

    def format_mean_std(mean, std):
        best_vals = mean.nlargest(n=n_top).index
        if mean.name == 'Rank':
            best_vals = mean.nsmallest(n=n_top).index
        vals_print = [f'{m:.2f}±{s:.2f}' for m, s in zip(mean, std)]
        vals_print = [f'\\textbf{{{el}}}' if idx in best_vals else el for idx, el in zip(mean.index, vals_print)]
        return vals_print

    df_combined = pd.DataFrame(index=df_mean.index)
    for col in df_mean.columns:
        df_combined[col] = format_mean_std(df_mean[col], df_std[col])
    df_combined.columns = pd.MultiIndex.from_tuples([(f'Per {grouping}', el) for el in df_combined.columns])
    df_combined.index.name = None

    df_tmp = df_performance[df_performance['Metric'].isin(metrics)]
    df_tmp = df_tmp[df_tmp['Group']=='full_data']
    df_tmp = df_tmp.groupby(['BaseModel', 'Metric'])['Value'].mean().unstack()
    for col in metrics:
        if col not in df_tmp.columns:
            df_tmp[col] = '-'
    df_tmp = df_tmp[metrics]
    def format_mean(mean, n_top=3):
        cat_models_lower = ['mixtcrpred', 'nettcrcat', 'tcrgp']
        mean_ = mean[~mean.index.isin(cat_models_lower)]
        best_vals = mean_.nlargest(n=n_top).index
        if mean.name == 'Rank':
            best_vals = mean_.nsmallest(n=n_top).index
        vals_print = [f'{m:.2f}' for m in mean]
        vals_print = [el + '*' if idx in cat_models_lower else el
                      for idx, el in zip(mean.index, vals_print)]
        vals_print = [f'\\textbf{{{el}}}' if idx in best_vals else el
                     for idx, el in zip(mean.index, vals_print)]
        return vals_print
    if len(df_tmp) > 0:
        df_tmp = df_tmp.apply(format_mean, axis=0)
    df_tmp.columns = pd.MultiIndex.from_tuples([('Full Data', el) for el in df_tmp.columns])
    df_tmp.index.name = None

    df_tmp = pd.concat([df_tmp, df_combined], axis=1)
    df_tmp.index = df_tmp.index.map(mapper_methods)
    df_tmp = df_tmp.fillna("-")
    
    df_tmp.index = ['\\textbf{' + el + '}' if el in cat_models else el for el in df_tmp.index]
    
    return df_tmp



def to_latex_string(df):
    init = [r"\begin{table}[ht]",
            r"\resizebox{\textwidth}{!}{%}",
            r"\centering",
            r"\begin{tabular}{" + " ".join(["l"] + ["l"] * (len(df.columns)//2-1) + ["l |"] + ["l"]*(len(df.columns)//2)) + "}",
            r"\toprule"]
    top_header = [""]
    for el in df.columns:
        top_header.append(el[0] if el[0] not in top_header else " ")
    header = [
        " & ".join(top_header) + " \\\\",
        " & ".join([" "] + [el[1] for el in df.columns]) + " \\\\",
        '\midrule'
    ]
    body = [" & ".join([el.name] + el.values.tolist()) + " \\\\" for _, el in df.iterrows()]
    end = ["\\bottomrule",
           "\end{tabular}}",
           "\caption{\\textbf{}}",
           "\label{}",
           "\end{table}"]
    
    cmd =  init + header + body + end
    for line in cmd:
        print(line)

