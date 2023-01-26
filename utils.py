# really bad functions name and docstrings for now
import pandas as pd

def foo(d: dict, l_filter: list[str]) -> dict:
    
    """
    Gets the dictionary and the list of keys to filter.
    
    >>> d = foo({'a':1, 'b':2, 'c':3}, ['a', 'c'])
    >>> d
    {'a':1, 'c':3}
    
    """
    
    return {k:v for k,v in d.items() if k in l_filter}

def foo1(d: dict) -> dict:
    
    """
    In the "genres" key, the value is a list of dictionaries and the only key we want is "name"
    which is the name of the genre.
    """
    
    return {k:(v if not k in ['genres', 'demographics'] else [i['name'] for i in v]) for k,v in d.items()}


def pandas_explode(df: pd.DataFrame, column_name: str) -> tuple[pd.DataFrame, list[str]]:
    df = df.join(pd.crosstab((s:=df[column_name].explode()).index, s))
    return df, df[column_name].explode().unique()