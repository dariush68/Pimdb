from django.conf.urls import url
from . import views

app_name = 'Core'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home$', views.home, name='home'),
    url(r'^moviesingle$', views.moviesingle, name='moviesingle'),
    url(r'^moviegrid$', views.moviegrid, name='moviegrid'),
    url(r'^moviegridfw$', views.moviegridfw, name='moviegridfw'),
    url(r'^movielist$', views.movielist, name='movielist'),
    url(r'^movie/(?P<movie_id>[0-9]+)$', views.movie, name='movie-single'),
    url(r'^seriessingle$', views.seriessingle, name='seriessingle'),
    url(r'^celebritygrid$', views.celebritygrid, name='celebritygrid'),
    url(r'^celebritygridsmall$', views.celebritygridsmall, name='celebritygridsmall'),
    url(r'^celebritylist$', views.celebritylist, name='celebritylist'),
    url(r'^celebritysingle$', views.celebritysingle, name='celebritysingle'),
    url(r'^celebrity/(?P<celebrity_id>[0-9]+)$', views.celebrity, name='celebrity'),
    url(r'^bloglist$', views.bloglist, name='bloglist'),
    url(r'^bloggrid$', views.bloggrid, name='bloggrid'),
    url(r'^blogdetail/(?P<blog_id>[0-9]+)$', views.blogdetail, name='blogdetail'),
    url(r'^userfavoritegrid$', views.userfavoritegrid, name='userfavoritegrid'),
    url(r'^userfavoritelist$', views.userfavoritelist, name='userfavoritelist'),
    url(r'^userprofile$', views.userprofile, name='userprofile'),
    url(r'^userrate$', views.userrate, name='userrate'),
    url(r'^page404$', views.page404, name='page404'),
    url(r'^comingsoon$', views.comingsoon, name='comingsoon'),
    url(r'^feed$', views.feed, name='feed'),
]
