from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from PyMovieDb import IMDB


@login_required
def home(request):
    return render(request, 'home.html')

def search(request):
    print("search view")
    db = IMDB()
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', '')
    if search_type == 'movieSearch':
        results = db.search(query)["results"]
    elif search_type == 'tvSearch':
        results = db.search(query, tv=True)["results"]
    if search_type == 'movieSearch':
        results = [r for r in results if r['media_type'] == 'Movie']
    for result in results:
        # print all the results
        if search_type == 'movieSearch':
            print(f"title: {result['title']}, year: {result['year']}, id: {result['id']}, leads: {result['leads']}, type: {result['media_type']}\nposter: {result['poster']}\n")
        print(f"title: {result['title']}, year: {result['year']}, id: {result['id']}, leads: {result['leads']}, type: {result['media_type']}\nposter: {result['poster']}\n")
    return JsonResponse({"results": results})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('player')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')