import requests
import time
from constants import SLEEP_VALUE
from utils import foo, foo1
from typing import Iterator
from itertools import chain

class MAL_extractor:
    
    """
    Really simple MAL extractor. It only loads information about animes that the user has in it list.
    Could use the API but for now I just wanted to get primarily "plan to watch" and "completed" animes.
    """
    

    url = 'https://myanimelist.net/animelist/{name}/load.json?offset={offset_value}&status={status}'

    # for now the useful items we could use for the model.
    keys_to_get = ['score', 'anime_title_eng', 
                   'anime_season', 'anime_score_val', 
                   'genres', 'demographics', 
                   'anime_url', 'anime_media_type_string',
                   'anime_mpaa_rating_string', 'anime_title']

    def __init__(self, user_name: str, status: int = 2) -> None:
        
        """
        Attributes:
        user_name: str
            the user name of the MAL account
        status: int
            which data to get, if its the completed, on hold, dropped, etc.
            status=2 means completed
            status=1 means watching
            status=3 means on hold
            status=4 means dropped
            status=6 means plan to watch
    
        """
        
        self.user_name = user_name
        self.status = status
        pass
    
    def request_url(self, 
                    offset_value: int):
        """
        Wrapper for the request.get function
        It just adds the offset value and the status to the url.
        In the MAL api if you set offset_value to = 0, it will return the first 300 animes.
        to get the next 300 animes you need to set offset_value to = 300, and so on.
        """
        return requests.get(self.url.format(name=self.user_name, offset_value=offset_value, status=self.status))

    def recursive_request(self, 
                          offset_value: int = 0) -> Iterator[dict]:
        
        """
        This function is a generator that will yield the data from the request.
        It just get the request_url function and yield all animes from the user.
        """

        while True:
            time.sleep(SLEEP_VALUE)
            response = self.request_url(offset_value)
            response_json = response.json()
            # if status_code != 200 raise
            if (response.status_code == 200) and (response_json):
                yield response.json()
                offset_value += 300
            else:
                break
            
    def get_data(self) -> list[dict]:
        
        """
        After getting the data from the recursive_request function, this function will return a list of all animes.
        Works to execute the generator function. This one returns ALL the keys from the MAL website.
        """
        
        # it's possible to have only 2 lists, its better to add both than to use chain
        return list(chain.from_iterable(self.recursive_request()))
        

    def refined_data(self) -> list[dict]:
        
        """
        This is the refined data for the model.
        Filters all the items we want and returns a list of dictionaries with the anime list information.
        """
        
        data = self.get_data()
        # chain functions
        data = [foo(d, self.keys_to_get) for d in data]
        data = [foo1(d) for d in data]
        return data