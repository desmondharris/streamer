import django
import tmdbsimple as tmdb
import os
# tmdb.API_KEY = '16d0db51d9356bcbecc06f57c1c0e593'
# config = tmdb.Configuration()
# searcher = tmdb.Search()
# print(searcher.tv(query="the office"))
# for s in searcher.results:
#     print(s['title'], s['id'], s['release_date'], s['popularity'])
from home.models import WatchedTV
WatchedTV.objects.all().delete()
