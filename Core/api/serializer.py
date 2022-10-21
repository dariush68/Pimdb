from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth.models import User
from Core import models
from django.db.models import F


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'date_joined',
            'is_active',
            'is_staff'
        ]
        read_only_fields = ('is_active', 'is_staff', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = [
            'id',
            'title',
            'title_en',
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = [
            'id',
            'title',
            'title_en',
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = [
            'id',
            'title',
            'title_en',
        ]


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cast
        fields = [
            'id',
            'title',
            'title_en',
        ]


class ArticleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArticleCategory
        fields = [
            'id',
            'title',
            'title_en',
        ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = [
            'id',
            'title',
            'title_en',
        ]


class MovieGenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.SerializerMethodField(read_only=True)
    movie_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.MovieGenre
        fields = [
            'id',
            'genre',
            'genre_name',
            'movie',
            'movie_name',
        ]

    def get_genre_name(self, obj):
        return obj.genre.title

    def get_movie_name(self, obj):
        return obj.movie.title


class MovieGenreLightSerializer(serializers.ModelSerializer):
    genre_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.MovieGenre
        fields = [
            'id',
            'genre',
            'genre_name',
        ]

    def get_genre_name(self, obj):
        return obj.genre.title


class MoviePosterSerializer(serializers.ModelSerializer):
    movie_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.MoviePoster
        fields = [
            'id',
            'title',
            'title_en',
            'image',
            'thumbnail',
            'movie',
            'movie_name',
            'created_on',
        ]

    def get_movie_name(self, obj):
        return obj.movie.title


class MovieTrailerSerializer(serializers.ModelSerializer):
    movie_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.MovieTrailer
        fields = [
            'id',
            'title',
            'title_en',
            'trailer',
            'thumbnail',
            'duration',
            'movie',
            'movie_name',
            'created_on',
        ]

    def get_movie_name(self, obj):
        return obj.movie.title


class MovieCommentSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField(read_only=True)
    comment_message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.MovieComment
        fields = [
            'id',
            'movie',
            'movie_title',
            'comment',
            'comment_message',
        ]

    def get_movie_title(self, obj):
        return obj.movie.title

    def get_comment_message(self, obj):
        return obj.comment.message


class MovieReviewSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField(read_only=True)
    review_message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.MovieReview
        fields = [
            'id',
            'movie',
            'movie_title',
            'review',
            'review_message',
        ]

    def get_movie_title(self, obj):
        return obj.movie.title

    def get_review_message(self, obj):
        return obj.review.review


class MovieCastSerializer(serializers.ModelSerializer):
    movie_title = serializers.SerializerMethodField(read_only=True)
    actor_name = serializers.SerializerMethodField(read_only=True)
    actor_photo = serializers.SerializerMethodField(read_only=True)
    cast_title = serializers.SerializerMethodField(read_only=True)
    movie_url = serializers.SerializerMethodField(read_only=True)
    movie_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.MovieCast
        fields = [
            'id',
            'role',
            'priority',
            'created_on',
            'movie',
            'movie_title',
            'actor',
            'actor_name',
            'actor_photo',
            'cast',
            'cast_title',
            'movie_url',
            'movie_date',
        ]

    def get_movie_title(self, obj):
        return obj.movie.title

    def get_actor_name(self, obj):
        return f'{obj.actor.name} {obj.actor.family}'

    def get_actor_photo(self, obj):
        return obj.actor.image.url

    def get_cast_title(self, obj):
        return obj.cast.title

    def get_movie_url(self, obj):
        return obj.movie.image.url

    def get_movie_date(self, obj):
        return obj.movie.created_on


class MovieSerializer(serializers.ModelSerializer):
    rate_star = serializers.SerializerMethodField(read_only=True)
    vote_count = serializers.SerializerMethodField(read_only=True)
    movieGenre = MovieGenreLightSerializer(many=True)

    class Meta:
        model = models.Movie
        fields = [
            'id',
            'title',
            'title_en',
            'movieGenre',
            'image',
            'thumbnail',
            'duration',
            'created_on',
            'rate',
            'rate_star',
            'vote_count',
            'view_count',
            'download_count',
            'abstract',
        ]

    def get_rate_star(self, obj):
        # models.Movie.objects.filter(id=obj.id).update(view_count=F('view_count')+1)
        return obj.userRates.aggregate(Avg('rate'))

    def get_vote_count(self, obj):
        return obj.userRates.count()


class MovieWithCastSerializer(serializers.ModelSerializer):
    rate_star = serializers.SerializerMethodField(read_only=True)
    movieCasts = MovieCastSerializer(many=True)

    class Meta:
        model = models.Movie
        fields = [
            'id',
            'title',
            'title_en',
            'image',
            'thumbnail',
            'duration',
            'created_on',
            'rate',
            'rate_star',
            'view_count',
            'download_count',
            'abstract',
            'movieCasts',
        ]

    def get_rate_star(self, obj):
        # models.Movie.objects.filter(id=obj.id).update(view_count=F('view_count')+1)
        return obj.userRates.aggregate(Avg('rate'))


class MovieDetailSerializer(serializers.ModelSerializer):
    rate_star = serializers.SerializerMethodField(read_only=True)
    vote_count = serializers.SerializerMethodField(read_only=True)
    movieGenre = MovieGenreLightSerializer(many=True)
    moviePoster = MoviePosterSerializer(many=True)
    movieTrailer = MovieTrailerSerializer(many=True)
    movieComments = MovieCommentSerializer(many=True)
    movieReviews = MovieReviewSerializer(many=True)
    movieCasts = MovieCastSerializer(many=True)

    class Meta:
        model = models.Movie
        fields = [
            'id',
            'title',
            'title_en',
            'movieGenre',
            'image',
            'thumbnail',
            'duration',
            'created_on',
            'rate',
            'rate_star',
            'vote_count',
            'view_count',
            'download_count',
            'abstract',
            'moviePoster',
            'movieTrailer',
            'movieComments',
            'movieReviews',
            'movieCasts',
        ]

    def get_rate_star(self, obj):
        # models.Movie.objects.filter(id=obj.id).update(view_count=F('view_count')+1)
        return obj.userRates.aggregate(Avg('rate'))

    def get_vote_count(self, obj):
        return obj.userRates.count()


class ActorSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Actor
        fields = [
            'id',
            'country',
            'city_name',
            # 'clinicsOfGroup',
            # 'clinicsAgent',
            'name',
            'name_en',
            'family',
            'family_en',
            'image',
            'thumbnail',
            'birthDay',
            'bio',
            'bio_short',
            'bio_en',
        ]

    def get_city_name(self, obj):
        if obj.city is not None:
            return obj.city.title


class ActorMoviePosterSerializer(serializers.ModelSerializer):
    moviePoster_poster = serializers.SerializerMethodField(read_only=True)
    actor_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.ActorMoviePoster
        fields = [
            'id',
            'moviePoster',
            'moviePoster_poster',
            'actor',
            'actor_name',
        ]

    def get_moviePoster_poster(self, obj):
        return obj.moviePoster.poster.url

    def get_actor_name(self, obj):
        return f'{obj.actor.name} {obj.actor.family}'


class ActorMovieTrailerSerializer(serializers.ModelSerializer):
    movieTrailer_trailer = serializers.SerializerMethodField(read_only=True)
    actor_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.ActorMovieTrailer
        fields = [
            'id',
            'movieTrailer',
            'movieTrailer_trailer',
            'actor',
            'actor_name',
        ]

    def get_movieTrailer_trailer(self, obj):
        return obj.movieTrailer.trailer.url

    def get_actor_name(self, obj):
        return f'{obj.actor.name} {obj.actor.family}'


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Comment
        fields = [
            'id',
            'created_on',
            'message',
            'rate',
            'user',
            'user_name',
        ]

    def get_user_name(self, obj):
        return obj.user.username


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Review
        fields = [
            'id',
            'created_on',
            'review',
            'rate',
            'user',
            'user_name',
        ]

    def get_user_name(self, obj):
        return obj.user.username


class EpisodeSerializer(serializers.ModelSerializer):
    season_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Episode
        fields = [
            'id',
            'number',
            'image',
            'thumbnail',
            'duration',
            'title',
            'title_en',
            'created_on',
            'season',
            'season_title',
        ]

    def get_season_title(self, obj):
        return obj.season.title


class SeriesGenreSerializer(serializers.ModelSerializer):
    genre_name = serializers.SerializerMethodField(read_only=True)
    series_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.SeriesGenre
        fields = [
            'id',
            'genre',
            'genre_name',
            'series',
            'series_title',
        ]

    def get_genre_name(self, obj):
        return obj.genre.title

    def get_series_title(self, obj):
        return obj.series.title


class SeriesGenreLightSerializer(serializers.ModelSerializer):
    genre_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.SeriesGenre
        fields = [
            'id',
            'genre',
            'genre_name',
        ]

    def get_genre_name(self, obj):
        return obj.genre.title


class SeriesPosterSerializer(serializers.ModelSerializer):
    series_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.SeriesPoster
        fields = [
            'id',
            'title',
            'title_en',
            'image',
            'thumbnail',
            'series',
            'series_title',
            'created_on',
        ]

    def get_series_title(self, obj):
        return obj.series.title


class SeriesTrailerSerializer(serializers.ModelSerializer):
    series_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.SeriesTrailer
        fields = [
            'id',
            'trailer',
            'title_en',
            'trailer',
            'thumbnail',
            'duration',
            'series',
            'series_title',
            'created_on',
        ]

    def get_series_title(self, obj):
        return obj.series.title


class SeriesCommentSerializer(serializers.ModelSerializer):
    series_title = serializers.SerializerMethodField(read_only=True)
    comment_message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.SeriesComment
        fields = [
            'id',
            'series',
            'series_title',
            'comment',
            'comment_message',
        ]

    def get_series_title(self, obj):
        return obj.series.title

    def get_comment_message(self, obj):
        return obj.comment.message


class SeriesCastSerializer(serializers.ModelSerializer):
    series_title = serializers.SerializerMethodField(read_only=True)
    actor_name = serializers.SerializerMethodField(read_only=True)
    cast_title = serializers.SerializerMethodField(read_only=True)
    series_url = serializers.SerializerMethodField(read_only=True)
    series_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.SeriesCast
        fields = [
            'id',
            'role',
            'priority',
            'created_on',
            'series',
            'series_title',
            'actor',
            'actor_name',
            'cast',
            'cast_title',
            'series_url',
            'series_date',
        ]

    def get_series_title(self, obj):
        return obj.series.title

    def get_actor_name(self, obj):
        return f'{obj.actor.name} {obj.actor.family}'

    def get_cast_title(self, obj):
        return obj.cast.title

    def get_series_url(self, obj):
        return obj.series.poster.url

    def get_series_date(self, obj):
        return obj.series.created_on


class SeriesReviewSerializer(serializers.ModelSerializer):
    series_title = serializers.SerializerMethodField(read_only=True)
    review_message = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.SeriesReview
        fields = [
            'id',
            'series',
            'series_title',
            'review',
            'review_message',
        ]

    def get_series_title(self, obj):
        return obj.series.title

    def get_review_message(self, obj):
        return obj.review.review


class SeriesSerializer(serializers.ModelSerializer):
    rate_star = serializers.SerializerMethodField(read_only=True)
    vote_count = serializers.SerializerMethodField(read_only=True)
    seriesGenres = SeriesGenreLightSerializer(many=True)

    class Meta:
        model = models.Series
        fields = [
            'id',
            'title',
            'title_en',
            'seriesGenres',
            'image',
            'thumbnail',
            'created_on',
            'rate',
            'rate_star',
            'vote_count',
            'view_count',
            'download_count',
            'abstract',
        ]

    def get_rate_star(self, obj):
        # models.Movie.objects.filter(id=obj.id).update(view_count=F('view_count')+1)
        return obj.userRates.aggregate(Avg('rate'))

    def get_vote_count(self, obj):
        return obj.userRates.count()


class SeasonSerializer(serializers.ModelSerializer):
    series_title = serializers.SerializerMethodField(read_only=True)
    seasonEpisodes = EpisodeSerializer(many=True)

    class Meta:
        model = models.Season
        fields = [
            'id',
            'number',
            'image',
            'thumbnail',
            'title',
            'title_en',
            'created_on',
            'series',
            'series_title',
            'seasonEpisodes',
        ]

    def get_series_title(self, obj):
        return obj.series.title


class SeriesDetailSerializer(serializers.ModelSerializer):
    rate_star = serializers.SerializerMethodField(read_only=True)
    vote_count = serializers.SerializerMethodField(read_only=True)
    seriesGenres = SeriesGenreLightSerializer(many=True)
    seriesSeasons = SeasonSerializer(many=True)
    seriesPosters = SeriesPosterSerializer(many=True)
    seriesTrailers = SeriesTrailerSerializer(many=True)
    seriesComments = SeriesCommentSerializer(many=True)
    seriesCasts = SeriesCastSerializer(many=True)
    seriesReviews = SeriesReviewSerializer(many=True)

    class Meta:
        model = models.Series
        fields = [
            'id',
            'title',
            'title_en',
            'seriesGenres',
            'image',
            'thumbnail',
            'created_on',
            'rate',
            'rate_star',
            'vote_count',
            'view_count',
            'download_count',
            'abstract',
            'seriesSeasons',
            'seriesPosters',
            'seriesTrailers',
            'seriesComments',
            'seriesCasts',
            'seriesReviews',
        ]

    def get_rate_star(self, obj):
        # models.Movie.objects.filter(id=obj.id).update(view_count=F('view_count')+1)
        return obj.userRates.aggregate(Avg('rate'))

    def get_vote_count(self, obj):
        return obj.userRates.count()


class SeriesWithCastSerializer(serializers.ModelSerializer):
    rate_star = serializers.SerializerMethodField(read_only=True)
    seriesCasts = SeriesCastSerializer(many=True)

    class Meta:
        model = models.Series
        fields = [
            'id',
            'title',
            'title_en',
            'image',
            'thumbnail',
            'created_on',
            'rate',
            'rate_star',
            'view_count',
            'download_count',
            'abstract',
            'seriesCasts',
        ]

    def get_rate_star(self, obj):
        # models.Movie.objects.filter(id=obj.id).update(view_count=F('view_count')+1)
        return obj.userRates.aggregate(Avg('rate'))


class ArticleSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)
    series_title = serializers.SerializerMethodField(read_only=True)
    movie_title = serializers.SerializerMethodField(read_only=True)
    articleCategory_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Article
        fields = [
            'id',
            'user',
            'user_name',
            'series',
            'series_title',
            'movie',
            'movie_title',
            'articleCategory',
            'articleCategory_title',
            'title',
            'title_en',
            'image',
            'thumbnail',
            'created_on',
        ]

    def get_user_name(self, obj):
        return obj.user.username

    def get_series_title(self, obj):
        return obj.series.title if obj.series else ""

    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else ""

    def get_articleCategory_title(self, obj):
        return obj.articleCategory.title


class ArticleTagSerializer(serializers.ModelSerializer):
    article_title = serializers.SerializerMethodField(read_only=True)
    tag_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.ArticleTag
        fields = [
            'id',
            'article',
            'article_title',
            'tag',
            'tag_title',
        ]

    def get_article_title(self, obj):
        return obj.article.title

    def get_tag_title(self, obj):
        return obj.tag.title


class ArticleCommentSerializer(serializers.ModelSerializer):
    article_title = serializers.SerializerMethodField(read_only=True)
    comment_message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.ArticleComment
        fields = [
            'id',
            'article',
            'article_title',
            'comment',
            'comment_message',
        ]

    def get_article_title(self, obj):
        return obj.article.title

    def get_comment_message(self, obj):
        return obj.comment.message


class UserFavoriteSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)

    series = SeriesWithCastSerializer()
    movie = MovieWithCastSerializer()

    class Meta:
        model = models.UserFavorite
        fields = [
            'id',
            'user',
            'user_name',
            'series',
            'movie',
            'created_on',
        ]
        depth = 0

    def get_user_name(self, obj):
        return obj.user.username


class UserRateSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField(read_only=True)

    series = SeriesWithCastSerializer()
    movie = MovieWithCastSerializer()

    class Meta:
        model = models.UserRate
        fields = [
            'id',
            'user',
            'user_name',
            'series',
            'movie',
            'created_on',
            'rate',
        ]

    def get_user_name(self, obj):
        return obj.user.username


class ActorDetailSerializer(serializers.ModelSerializer):
    actorMoviePosters = ActorMoviePosterSerializer(many=True)
    actorMovieTrailers = ActorMovieTrailerSerializer(many=True)
    movieCasts = MovieCastSerializer(many=True)
    seriesCasts = SeriesCastSerializer(many=True)

    class Meta:
        model = models.Actor
        fields = [
            'id',
            'country',
            'city',
            # 'clinicsOfGroup',
            # 'clinicsAgent',
            'name',
            'name_en',
            'family',
            'family_en',
            'image',
            'thumbnail',
            'birthDay',
            'bio',
            'bio_short',
            'bio_en',
            'actorMoviePosters',
            'actorMovieTrailers',
            'movieCasts',
            'seriesCasts',
        ]

