from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en", "series", "movie", "articleCategory", "created_on")
    list_filter = ("title",  "series", "movie", "articleCategory", "created_on")
    search_fields = ('title', 'series', 'movie', )


@admin.register(models.Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en", "rate", "created_on")
    list_filter = ("title",  "title_en", "rate", "created_on")
    search_fields = ("title",  "title_en", )


@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en", "duration", "rate", "download_count", "view_count", "created_on")
    list_filter = ("title",  "title_en", "duration", "rate", "download_count", "view_count", "created_on")
    search_fields = ("title",  "title_en", )


@admin.register(models.ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en")
    list_filter = ("title",  "title_en")


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en")
    list_filter = ("title",  "title_en")


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en")
    list_filter = ("title",  "title_en")


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en")
    list_filter = ("title",  "title_en")


@admin.register(models.MovieGenre)
class MovieGenreAdmin(admin.ModelAdmin):
    list_display = ("id", "genre", "movie")
    list_filter = ("genre",  "movie")


@admin.register(models.MoviePoster)
class MoviePosterAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "title", "title_en", "created_on")
    list_filter = ("movie",  "created_on")


@admin.register(models.MovieTrailer)
class MovieTrailerAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "title", "title_en", "trailer", "duration", "created_on")
    list_filter = ("movie",  "created_on")


@admin.register(models.Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "family", "country", "city", "birthDay")
    list_filter = ("country",  "city")
    search_fields = ("name",  "family", )
    # list_select_related = ['city__title']
    # raw_id_fields = ("country",)


@admin.register(models.ActorMoviePoster)
class ActorMoviePosterAdmin(admin.ModelAdmin):
    list_display = ("id", "moviePoster", "actor")
    list_filter = ("moviePoster",  "actor")


@admin.register(models.ActorMovieTrailer)
class ActorMovieTrailerAdmin(admin.ModelAdmin):
    list_display = ("id", "movieTrailer", "actor")
    list_filter = ("movieTrailer",  "actor")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "rate", "created_on")
    list_filter = ("user",  "rate",  "created_on")


@admin.register(models.MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "comment")
    list_filter = ("movie", )


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "review", "rate", "created_on")
    list_filter = ("user",  "rate",  "created_on")


@admin.register(models.MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "review")
    list_filter = ("movie", "review")


@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en")
    list_filter = ("title",)


@admin.register(models.MovieCast)
class MovieCastAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "actor", "cast", "role", "priority", "created_on")
    list_filter = ("movie", "actor", "cast", "role", "priority", "created_on")


@admin.register(models.Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ("id", "series", "number", "title", "created_on")
    list_filter = ("series", "number", "title", "created_on")


@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ("id", "season", "number", "title", "created_on")
    list_filter = ("season", "number", "title", "created_on")


@admin.register(models.SeriesGenre)
class SeriesGenreAdmin(admin.ModelAdmin):
    list_display = ("id", "genre", "series")
    list_filter = ("genre", "series")


@admin.register(models.SeriesPoster)
class SeriesPosterAdmin(admin.ModelAdmin):
    list_display = ("id", "series", "created_on")
    list_filter = ("series", "created_on")


@admin.register(models.SeriesTrailer)
class SeriesTrailerAdmin(admin.ModelAdmin):
    list_display = ("id", "trailer", "series", "created_on")
    list_filter = ("trailer", "series", "created_on")


@admin.register(models.SeriesComment)
class SeriesCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "series",)
    list_filter = ("series", )


@admin.register(models.SeriesCast)
class SeriesCastAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "series", "cast", "role", "priority", "created_on")
    list_filter = ("series", "actor", "cast", "role",  "priority", "created_on")


@admin.register(models.SeriesReview)
class SeriesReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "series", "created_on")
    list_filter = ("series", "created_on")


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "title_en")
    # list_filter = ()


@admin.register(models.ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "tag")
    list_filter = ("article", "tag")


@admin.register(models.ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "comment")
    list_filter = ("article", )


@admin.register(models.UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "series", "movie", "created_on")
    list_filter = ("user", "series", "movie", "created_on")


@admin.register(models.UserRate)
class UserRateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "series", "movie", "rate", "created_on")
    list_filter = ("user", "series", "movie", "rate", "created_on")


@admin.register(models.MovieInTheatre)
class MovieInTheatreAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "end_on", "created_on")
    list_filter = ("movie", "end_on", "created_on")


@admin.register(models.SpoliightActor)
class SpoliightActorAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "is_show")
    list_filter = ("actor", "is_show")


@admin.register(models.SpoliightMovie)
class SpoliightMovieAdmin(admin.ModelAdmin):
    list_display = ("id", "movie", "is_show")
    list_filter = ("movie", "is_show")


@admin.register(models.MovieCountry)
class MovieCountryAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "movie")
    list_filter = ("country", "movie")


@admin.register(models.MovieTag)
class MovieTagAdmin(admin.ModelAdmin):
    list_display = ("id", "tag", "movie")
    list_filter = ("tag", "movie")
