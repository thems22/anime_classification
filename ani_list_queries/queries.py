# QUERY for the anilist api to search for animes
QUERY = '''
query ($type: MediaType = ANIME, $page: Int = 1, $perPage: Int = 50) {
  Page(page: $page, perPage: $perPage) {
    media(type: $type, sort: SCORE_DESC) {
      id
      title {
        romaji
        english
        native
        userPreferred
      }
      genres
      tags {
        name
        rank
      }
    }
  }
}

'''

# QUERY for the anilist api to get the user list
QUERY_USER = '''
query ($id: Int, $name:String = "thems22", $type:MediaType = ANIME){
  MediaListCollection(userId:$id, userName: $name, type: $type){
    lists {
      entries{
        mediaId
        status
        score
        media{
          genres
          description
          popularity
          meanScore
          averageScore
          tags {
            name
            rank
          }
          title {
            romaji
            english
            native
            userPreferred
          }
        }
      }
    }
  }
}


'''