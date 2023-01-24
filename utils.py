# really bad functions name and docstrings for now

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