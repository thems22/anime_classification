from typing import Any
import requests
from constants import QUERY
import time

class AniList:
    
    """
    The genres in myanimelist aren't enough to make a good classification model.
    In the anilist website we can find more genres and tags.
    
    API limitations:
    only 90 requests per minute.
    
    TODO: 
    NEED to check if it didn't loaded all animes because of the limit.
    when it reaches the limit, it returns back a response error, for now the class just get that response
    and goes to load the next anime.
    For now I'm just adding random sleeps so it doesn't get blocked and I can load the data.
    """
    
    total_sleep = 30
    url = 'https://graphql.anilist.co'
    variables: dict[str, Any] = {
    'search': 'Fate/Zero', # the anime to search
    'page': 1, # the page to get
    'perPage': 10} #values per page
    
    def __init__(self, variables: dict[str, Any] = None,
                 multiple_search: list[str] = None) -> None:
        
        if variables: # we need to update the variables to the new searches we make.
            self.variables.update(variables)
            
        if multiple_search: # if we want to make multiple requests, pass a list of anime names.
            self.multiple_titles = multiple_search
            
        pass
    
    def get_json(self, name: str = None) -> dict[str, Any]:
        
        """
        Wrapper for the request.post function. It also updates the variables if we want to search for a specific anime.
        """
        
        if name:
            self.variables['search'] = name
        return requests.post(self.url, json={'query': QUERY, 'variables': self.variables}).json()
    
    def multiple_requests(self) -> dict[str, Any]:
        
        """
        We need to search for multiple animes.
        This seems to be horrible for now, but I had to do this because
        my list is from MAL.
        """
        
        for en, name in enumerate(self.multiple_titles, start=1):
            time.sleep(1)
            if en %90 == 0:
                time.sleep(self.total_sleep)
                self.total_sleep += 30
            yield self.get_json(name)
    
    def refined_data(self) -> dict[str, Any]:
        
        """
        just gather the actually useful (for now) data from the json.
        """
        
        data = self.get_json(None)
        return data['data']['Page']['media']
    