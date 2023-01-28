# QUERY for the anilist api to search for animes
QUERY = '''
query ($page: Int, $perPage: Int, $search: String, $format: MediaFormat = TV) {
  Page(page: $page, perPage: $perPage) {
    pageInfo {
      total
      currentPage
      lastPage
      hasNextPage
      perPage
    }
    media(search: $search, format: $format) {
      genres
      id
      idMal
      status
      seasonInt
      averageScore
      tags {
        name
        rank
        category
      }
      title {
        romaji
        english
        userPreferred
      }
    }
  }
}
'''

# QUERY for the anilist api to get the user list
QUERY_USER = '''
query ($id: Int, $name:String = "thems22"){
  MediaListCollection(userId:$id, userName: $name, type:ANIME){
    lists {
      entries{
        mediaId
        status
        score
        media{
          genres
          description
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