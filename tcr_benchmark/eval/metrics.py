import numpy as np
import pandas as pd
import warnings
from sklearn.metrics import roc_auc_score, average_precision_score, precision_recall_curve
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from scipy.stats import pearsonr, spearmanr, rankdata


SCORE_METRICS = {
    "AUC": roc_auc_score,
    "APS": average_precision_score,
}

CLASSIFICATION_METRICS = {
    "F1-Score": f1_score,
    "Accuracy": accuracy_score,
    "Precision": precision_score,
    "Recall": recall_score,
}

CORRELATION_METRICS = {
    "Pearson": pearsonr,
    "Spearman": spearmanr,
}


def recall_at_k(ranks, k):
    return np.mean(ranks <= k)


def calculate_score_metrics(labels, scores, groups=None):
    """
    Calculates metrics that can be calculated from a contineous score and binary label
    :param labels: iterable(int) indicating the ground truth
    :param scores: iterable(float) indicating the prediction score
    :param groups: iterable, indicating groups of predictions belonging together
    :return: dict(name_metric: score) resulting metrics
    """
    n_metrics = len(SCORE_METRICS)
    metric_names = list(SCORE_METRICS.keys())
    metric_values = [func(labels, scores) for func in SCORE_METRICS.values()]
    group_names = ["full_data"] * n_metrics
    support_values = [len(labels)] * n_metrics

    if groups is not None:
        for group in set(groups):
            mask = groups == group
            labels_tmp = labels[mask]
            scores_tmp = scores[mask]

            metric_names += list(SCORE_METRICS.keys())
            metric_values += [func(labels_tmp, scores_tmp) for func in SCORE_METRICS.values()]
            group_names += [group] * n_metrics
            support_values += [len(labels_tmp)] * n_metrics

    metrics = pd.DataFrame(data={
        "Group": group_names,
        "Support": support_values,
        "Metric": metric_names,
        "Value": metric_values
    })
    return metrics


def calculate_classification_metrics(labels, scores, groups=None):
    """
    Calculate metrics that can be calculated from discrete classification and binary label.
    The threshold will be choosen to optimize the F1-Score on the whole dataset.
    :param labels: iterable(int) indicating the ground truth
    :param scores: iterable(float) indicating the prediction score
    :param groups: iterable, indicating groups of predictions belonging together
    :return: dict(name_metric: score) resulting metrics
    """
    precisions, recalls, thresholds = precision_recall_curve(labels, scores)
    f1_scores = 2 * recalls * precisions / (recalls + precisions)
    threshold = thresholds[np.nanargmax(f1_scores)]
    y_pred = scores >= threshold

    n_metrics = len(CLASSIFICATION_METRICS)
    metric_names = list(CLASSIFICATION_METRICS.keys())
    metric_values = [func(labels, y_pred) for func in CLASSIFICATION_METRICS.values()]
    group_names = ["full_data"] * n_metrics
    support_values = [len(labels)] * n_metrics

    if groups is not None:
        for group in set(groups):
            mask = groups == group
            labels_tmp = labels[mask]
            y_pred_tmp = y_pred[mask]

            metric_names += list(CLASSIFICATION_METRICS.keys())
            metric_values += [func(labels_tmp, y_pred_tmp) for func in CLASSIFICATION_METRICS.values()]
            group_names += [group] * n_metrics
            support_values += [len(labels_tmp)] * n_metrics

    metrics = pd.DataFrame(data={
        "Group": group_names,
        "Support": support_values,
        "Metric": metric_names,
        "Value": metric_values
    })
    return metrics


def calculated_rank_metrics(labels, score_matrix, groups=None, ks=None):
    """

    :param labels:
    :param score_matrix:
    :param groups:
    :param ks:
    :params
    :return:
    """
    if ks is None:
        ks = []
    ranked = np.vstack([rankdata(row.values) for el, row in score_matrix.iterrows()])
    ranked = score_matrix.shape[1] - ranked + 1
    ranked = pd.DataFrame(data=ranked, index=score_matrix.index, columns=score_matrix.columns)


    mask_available = labels.values != ""
    delta = len(labels) - sum(mask_available)
    if delta != 0:
        warnings.warn(f"Filtering {delta} values as epitope prediction not available")
    labels = labels[mask_available]
    ranked = ranked[mask_available]

    ranks = [row[labels.iloc[i]] for i, (_, row) in enumerate(ranked.iterrows())]
    ranks = pd.DataFrame(data=ranks, columns=["rank"], index=labels.index)
    ranks["label"] = labels.values

    n_metrics = 1 + len(ks)
    metric_names = ["AverageRank"] + [f"R@{k}" for k in ks]
    metric_values = [np.mean(ranks["rank"])] + [recall_at_k(ranks["rank"], k) for k in ks]
    group_names = ["full_data"] * n_metrics
    support_values = [len(labels)] * n_metrics

    if groups is not None:
        for group in set(groups):
            mask = groups == group
            ranks_tmp = ranks[mask]

            metric_names += ["AverageRank"] + [f"R@{k}" for k in ks]
            metric_values += [np.mean(ranks_tmp["rank"])] + [recall_at_k(ranks_tmp["rank"], k) for k in ks]
            group_names += [group] * n_metrics
            support_values += [len(ranks_tmp)] * n_metrics

    metrics = pd.DataFrame(data={
        "Group": group_names,
        "Support": support_values,
        "Metric": metric_names,
        "Value": metric_values
    })
    return metrics


def calculate_correlation_metrics(labels, scores, groups=None):
    """
    Calculates metrics that can be calculated from a continuous score and continuous label
    :param labels: iterable(float) indicating the ground truth such as activation scores
    :param scores: iterable(float) indicating the prediction score
    :param groups: iterable, indicating groups of predictions belonging together
    :return: dict(name_metric: score) resulting metrics
    """
    n_metrics = len(CORRELATION_METRICS)
    metric_names = list(CORRELATION_METRICS.keys())
    metric_values = [func(labels, scores)[0] for func in CORRELATION_METRICS.values()]
    group_names = ["full_data"] * n_metrics
    support_values = [len(labels)] * n_metrics

    if groups is not None:
        for group in set(groups):
            mask = groups == group
            labels_tmp = labels[mask]
            scores_tmp = scores[mask]

            metric_names += list(CORRELATION_METRICS.keys())
            metric_values += [func(labels_tmp, scores_tmp)[0] for func in CORRELATION_METRICS.values()]
            group_names += [group] * n_metrics
            support_values += [len(labels_tmp)] * n_metrics

    metrics = pd.DataFrame(data={
        "Group": group_names,
        "Support": support_values,
        "Metric": metric_names,
        "Value": metric_values
    })
    return metrics
