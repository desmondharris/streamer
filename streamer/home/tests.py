import tmdbsimple as tmdb
tmdb.API_KEY = '16d0db51d9356bcbecc06f57c1c0e593'
config = tmdb.Configuration()
searcher = tmdb.Search()
print(searcher.movie(query="batman"))
for s in searcher.results:
    print(s['title'], s['id'], s['release_date'], s['popularity'])