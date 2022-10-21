from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import get_object_or_404
from . import models
from .feed import manzoom as FD


# first page
def index(request):
    movies_populate = models.Movie.objects.all().order_by('-download_count')[:20]
    movies_preBuild = models.Movie.objects.filter(Q(created_on__gte=datetime.now().date())).order_by('-download_count')[:20]
    movies_topRate = models.Movie.objects.all().order_by('-rate')[:20]
    movies_topView = models.Movie.objects.all().order_by('-view_count')[:20]

    series_populate = models.Series.objects.all().order_by('-download_count')[:20]
    series_preBuild = models.Series.objects.filter(Q(created_on__gte=datetime.now().date())).order_by('-download_count')[:20]
    series_topRate = models.Series.objects.all().order_by('-rate')[:20]
    series_topView = models.Series.objects.all().order_by('-view_count')[:20]

    movieInTheatre = models.MovieInTheatre.objects.all()

    news = models.Article.objects.all().order_by('-created_on')[:4]

    spolight_actors = models.SpoliightActor.objects.filter(is_show=True).order_by('-id')[:4]
    spolight_movie = models.SpoliightMovie.objects.filter(is_show=True).order_by('-id')

    return render(request, 'Core/index.html', {
        'movies_populate': movies_populate,
        'movies_preBuild': movies_preBuild,
        'movies_topRate': movies_topRate,
        'movies_topView': movies_topView,
        'series_populate': series_populate,
        'series_preBuild': series_preBuild,
        'series_topRate': series_topRate,
        'series_topView': series_topView,
        'movieInTheatre': movieInTheatre,
        'news': news,
        'spolight_actors': spolight_actors,
        'spolight_movie': spolight_movie,
    })


# first page
def home(request):
    return render(request, 'Core/home_wide.html', {})


# first page
def moviesingle(request):
    return render(request, 'Core/moviesingle.html', {})


# first page
def movie(request, movie_id):
    movie = get_object_or_404(models.Movie, pk=movie_id)
    return render(request, 'Core/moviesingle.html', {
        'movie': movie
    })


# first page
def moviegrid(request):
    return render(request, 'Core/moviegrid.html', {

        'page_title': 'لیست فیلم ها',
        'page_url': 'لیست فیلم ها',
        'page_url_en': 'movie-grid'
    })


# first page
def moviegridfw(request):
    return render(request, 'Core/moviegridfw.html', {

        'page_title': 'لیست فیلم ها',
        'page_url': 'لیست فیلم ها',
        'page_url_en': 'movie-grid-w'
    })


# first page
def movielist(request):
    return render(request, 'Core/movielist.html', {

        'page_title': 'لیست فیلم ها',
        'page_url': 'لیست فیلم ها',
        'page_url_en': 'movie-list'
    })


# first page
def seriessingle(request):
    return render(request, 'Core/seriessingle.html', {})


# first page
def celebritygrid(request):

    total = models.Actor.objects.count()
    casts = models.Cast.objects.all()
    return render(request, 'Core/celebritygrid.html', {
        'actor_count': total,
        'casts': casts,
        'page_title': 'لیست بازیگران - شبکه',
        'page_url': 'لیست بازیگران',
        'page_url_en': 'celebrity-grid'
    })


# first page
def celebritygridsmall(request):

    total = models.Actor.objects.count()
    casts = models.Cast.objects.all()
    return render(request, 'Core/celebritygridsmall.html', {
        'actor_count': total,
        'casts': casts,
        'page_title': 'لیست بازیگران - شبکه',
        'page_url': 'لیست بازیگران',
        'page_url_en': 'celebrity-grid-small'
    })


# first page
def celebritylist(request):

    total = models.Actor.objects.count()
    casts = models.Cast.objects.all()
    return render(request, 'Core/celebritylist.html', {
        'actor_count': total,
        'casts': casts,
        'page_title': 'لیست بازیگران',
        'page_url': 'لیست بازیگران',
        'page_url_en': 'celebrity-list'
    })


# first page
def celebritysingle(request):
    return render(request, 'Core/celebritysingle.html', {})


def celebrity(request, celebrity_id):

    obj = get_object_or_404(models.Actor, pk=celebrity_id)

    return render(request, 'Core/celebritysingle.html', {
        'actor': obj,
    })


# first page
def bloglist(request):
    return render(request, 'Core/bloglist.html', {})


# first page
def bloggrid(request):
    return render(request, 'Core/bloggrid.html', {})


# first page
def blogdetail(request, blog_id):
    return render(request, 'Core/blogdetail.html', {})


# first page
def userfavoritegrid(request):
    return render(request, 'Core/userfavoritegrid.html', {})


# first page
def userfavoritelist(request):
    return render(request, 'Core/userfavoritelist.html', {})


# first page
def userprofile(request):
    return render(request, 'Core/userprofile.html', {})


# first page
def userrate(request):
    return render(request, 'Core/userrate.html', {})


# first page
def page404(request):
    return render(request, 'Core/404.html', {})


# first page
def comingsoon(request):
    return render(request, 'Core/comingsoon.html', {})


def feed(request):
    FD.scrap_thread()
    return render(request, 'Core/comingsoon.html', {})
