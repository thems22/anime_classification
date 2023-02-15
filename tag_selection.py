from itertools import compress
import pandas as pd
import numpy as np
from sklearn.linear_model import Lasso
from sklearn.preprocessing import KBinsDiscretizer

# TODO: add more methods to select tags, and one method that merges more than one tag in a new feature.

def group_generator(scores: pd.Series, n_groups: int = 3):

    """
    The first step of our problem will always be something like this:
    reduce the number of scores to groups.
    """

    bins = KBinsDiscretizer(n_bins=n_groups, strategy='quantile', encode='ordinal')
    return bins.fit_transform(scores.values)

def lasso_method(X: pd.DataFrame, y: pd.Series, n_features: int = 15, verbose: bool = False, remove_less_than: int = 0):

    """
    the second step of our problem will always be around of reducing the number of features.
    """
    if remove_less_than > 0:
        X = remove_less(X, remove_less_than)
    coefs = []
    tags_columns = list(X.columns)
    for alpha in np.linspace(0.001, 0.1, 2000):
        lasso = Lasso(alpha=alpha, tol=1/1e9, max_iter=int(1e6))
        lasso.fit(X, y)
        coefs.append(lasso.coef_)
    data = pd.DataFrame(coefs, columns=tags_columns)
    data['dim_reducted'] = (data==0).sum(axis=1)
    min_possible = X.shape[1] - data['dim_reducted'].max()
    if verbose:
        print('min features possible',  min_possible)
    if n_features < min_possible:
        n_features = min_possible + 1 if n_features < min_possible else n_features
        print('n_features changed to', n_features)
    lasso_selected = list(compress(tags_columns,
                                   data[data['dim_reducted']>len(tags_columns)-n_features].iloc[0]!=0))

    return lasso_selected, data

def remove_less(X: pd.DataFrame, remove_ress_than: int):

    """
    simple column remover
    """
    
    
    x_columns = X.columns
    x_bool_columns = X[x_columns].sum() > remove_ress_than
    x_columns = compress(x_columns, x_bool_columns)

    return X[x_columns]
