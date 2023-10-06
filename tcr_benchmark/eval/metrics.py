import numpy as np
import warnings
from sklearn.metrics import roc_auc_score, average_precision_score, precision_recall_curve
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from scipy.stats import pearsonr, spearmanr


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


def calculate_score_metrics(labels, scores, groups=None):
    """
    Calculates metrics that can be calculated from a contineous score and binary label
    :param labels: iterable(int) indicating the ground truth
    :param scores: iterable(float) indicating the prediction score
    :param groups: iterable, indicating groups of predictions belonging together
    :return: dict(name_metric: score) resulting metrics
    """
    metrics = {name: func(labels, scores) for name, func in SCORE_METRICS.items()}
    if groups is not None:
        supports = {}
        for group in set(groups):
            mask = groups == group
            supports[group] = sum(mask & (labels == 1))
            labels_tmp = labels[mask]
            scores_tmp = scores[mask]
            metrics_tmp = {f"{name}_{group}": func(labels_tmp, scores_tmp) for name, func in SCORE_METRICS.items()}
            metrics.update(metrics_tmp)
        metrics_avg = {f"{name}_groups_avg": sum([metrics[f"{name}_{group}"]
                                                  for group in supports.keys()]) / len(supports)
                       for name in SCORE_METRICS.keys()}
        metrics_weighted = {f"{name}_groups_weighted": sum([metrics[f"{name}_{group}"] * supports[group]
                                                            / sum(supports.values())
                                                            for group in supports.keys()])
                            for name in SCORE_METRICS.keys()}
        metrics.update(metrics_avg)
        metrics.update(metrics_weighted)
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

    metrics = {}
    for name, func in CLASSIFICATION_METRICS.items():
        metrics[name] = func(labels, y_pred)

    if groups is not None:
        supports = {}
        for group in set(groups):
            mask = groups == group
            supports[group] = sum(mask & (labels == 1))
            labels_tmp = labels[mask]
            y_pred_tmp = y_pred[mask]
            metrics_tmp = {f"{name}_{group}": func(labels_tmp, y_pred_tmp)
                           for name, func in CLASSIFICATION_METRICS.items()}
            metrics.update(metrics_tmp)
        metrics_avg = {f"{name}_groups_avg": sum([metrics[f"{name}_{group}"]
                                                  for group in supports.keys()]) / len(supports)
                       for name in CLASSIFICATION_METRICS.keys()}
        metrics_weighted = {f"{name}_groups_weighted": sum([metrics[f"{name}_{group}"] * supports[group]
                                                            / sum(supports.values())
                                                            for group in supports.keys()])
                            for name in CLASSIFICATION_METRICS.keys()}
        metrics.update(metrics_avg)
        metrics.update(metrics_weighted)
    return metrics


def calculated_rank_metrics(labels, score_matrix, k_max=16):
    """

    :param labels:
    :param score_matrix:
    :return:
    """
    #scores_sorted = score_matrix.columns.values()
    #scores_sorted = score_matrix.columns.values[scores_sorted]
    #metrics = {}
    #for k in [1, 5, 10, 25, 50, k_max]:
    #    if k > k_max:
    #        continue
    #    r_at_k = label.isn
    # R@1, R@5, R@10
    # Avg rank
    #
    return {}


def calculate_correlation_metrics(labels, scores, groups=None):
    """
    Calculates metrics that can be calculated from a continuous score and continuous label
    :param labels: iterable(float) indicating the ground truth such as activation scores
    :param scores: iterable(float) indicating the prediction score
    :param groups: iterable, indicating groups of predictions belonging together
    :return: dict(name_metric: score) resulting metrics
    """
    metrics = {name: func(labels, scores)[0] for name, func in CORRELATION_METRICS.items()}
    if groups is not None:
        supports = {}
        for group in set(groups):
            mask = groups == group
            supports[group] = sum(mask & (labels == 1))
            labels_tmp = labels[mask]
            scores_tmp = scores[mask]
            metrics_tmp = {f"{name}_{group}": func(labels_tmp, scores_tmp)[0] for name, func in
                           CORRELATION_METRICS.items()}
            metrics.update(metrics_tmp)
        metrics_avg = {f"{name}_groups_avg": sum([metrics[f"{name}_{group}"]
                                                  for group in supports.keys()]) / len(supports)
                       for name in CORRELATION_METRICS.keys()}
        metrics_weighted = {f"{name}_groups_weighted": sum([metrics[f"{name}_{group}"] * supports[group]
                                                            / sum(supports.values())
                                                            for group in supports.keys()])
                            for name in CORRELATION_METRICS.keys()}
        metrics.update(metrics_avg)
        metrics.update(metrics_weighted)
    return metrics
