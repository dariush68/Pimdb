from rest_framework import viewsets, permissions
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from Core import models
from . import serializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class CountryViewset(viewsets.ModelViewSet):
    queryset = models.Country.objects.all()
    serializer_class = serializer.CountrySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        return qs


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializer.UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-date_joined')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            ).distinct()
        return qs


class CityViewset(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializer.CitySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        return qs


class GenreViewset(viewsets.ModelViewSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializer.GenreSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        return qs


class CastViewset(viewsets.ModelViewSet):
    queryset = models.Cast.objects.all()
    serializer_class = serializer.CastSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        return qs


class ArticleCategoryViewset(viewsets.ModelViewSet):
    queryset = models.ArticleCategory.objects.all()
    serializer_class = serializer.ArticleCategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        return qs


class TagViewset(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializer.TagSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        return qs


class MovieViewset(viewsets.ModelViewSet):
    queryset = models.Movie.objects.all()
    # serializer_class = serializer.MovieSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializer.MovieSerializer
        if self.action == 'retrieve':
            return serializer.MovieDetailSerializer
        return serializer.MovieSerializer  # create/destroy/update.

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')

        # Order
        query = self.request.GET.get("ordered_by")
        if query is not None:
            if query == "download_count":
                qs = qs.order_by('-download_count')
            elif query == "view_count":
                qs = qs.order_by('-view_count')
            elif query == "vote_count":
                qs = qs.order_by('-vote_count')
            elif query == "latest":
                qs = qs.order_by('-created_on')
            else:
                qs = qs.order_by('-id')

        # search
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        # Genre
        query = self.request.GET.get("genre")
        if query is not None:
            qs = qs.filter(
                Q(movieGenre__genre__title=query)
            ).distinct()
        # Rate
        query = self.request.GET.get("rate")
        if query is not None:
            qs = qs.filter(
                Q(rate=query)
            ).distinct()
        # Date
        query_date_from = self.request.GET.get("date_from")
        query_date_to = self.request.GET.get("date_to")
        if query_date_from is not None:
            qs = qs.filter(
                Q(created_on__gte=query_date_from)
            ).distinct()
        if query_date_to is not None:
            qs = qs.filter(
                Q(created_on__lte=query_date_to)
            ).distinct()
        # if query_date_from is not None and query_date_to is not None:
        #     qs = qs.filter(
        #         Q(created_on__range=[query_date_from, query_date_to])
        #     ).distinct()
        return qs


class MovieGenreViewset(viewsets.ModelViewSet):
    queryset = models.MovieGenre.objects.all()
    serializer_class = serializer.MovieGenreSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class MoviePosterViewset(viewsets.ModelViewSet):
    queryset = models.MoviePoster.objects.all()
    serializer_class = serializer.MoviePosterSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class MovieTrailerViewset(viewsets.ModelViewSet):
    queryset = models.MovieTrailer.objects.all()
    serializer_class = serializer.MovieTrailerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class ActorViewset(viewsets.ModelViewSet):
    queryset = models.Actor.objects.all()
    # serializer_class = serializer.ActorSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializer.ActorSerializer
        if self.action == 'retrieve':
            return serializer.ActorDetailSerializer
        return serializer.ActorSerializer  # create/destroy/update.

    def get_queryset(self):
        qs = super().get_queryset()

        # order
        query = self.request.GET.get("order")
        if query is not None:
            if query == "محبوبیت":
                qs.order_by('-download_count')
            if query == "بازدید":
                qs.order_by('-view_count')
            if query == "تولد":
                print('-birthDay')
                qs.order_by('-birthDay')
            else:
                qs.order_by('-id')


        # search
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query)
                | Q(name_en__icontains=query)
                | Q(family__icontains=query)
                | Q(family_en__icontains=query)
            ).distinct()

        # alphabet
        query = self.request.GET.get("alphabet")
        if query is not None:
            qs = qs.filter(
                Q(name__startswith=query)
                | Q(name_en__startswith=query)
                | Q(family__startswith=query)
                | Q(family_en__startswith=query)
            ).distinct()

        # cast
        query = self.request.GET.get("cast")
        if query is not None:
            qs = qs.filter(
                Q(movieCasts__cast__title=query)
            ).distinct()

        # Date
        query_date_from = self.request.GET.get("date_from")
        query_date_to = self.request.GET.get("date_to")
        if query_date_from is not None:
            print(query_date_from)
            qs = qs.filter(
                Q(birthDay__gte=query_date_from)
            ).distinct()
        if query_date_to is not None:
            print(query_date_to)
            qs = qs.filter(
                Q(birthDay__lte=query_date_to)
            ).distinct()
        return qs


class ActorMoviePosterViewset(viewsets.ModelViewSet):
    queryset = models.ActorMoviePoster.objects.all()
    serializer_class = serializer.ActorMoviePosterSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class ActorMovieTrailerViewset(viewsets.ModelViewSet):
    queryset = models.ActorMovieTrailer.objects.all()
    serializer_class = serializer.ActorMovieTrailerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class CommentViewset(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializer.CommentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class MovieCommentViewset(viewsets.ModelViewSet):
    queryset = models.MovieComment.objects.all()
    serializer_class = serializer.MovieCommentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializer.ReviewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class MovieReviewViewset(viewsets.ModelViewSet):
    queryset = models.MovieReview.objects.all()
    serializer_class = serializer.MovieReviewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class MovieCastViewset(viewsets.ModelViewSet):
    queryset = models.MovieCast.objects.all()
    serializer_class = serializer.MovieCastSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesViewset(viewsets.ModelViewSet):
    queryset = models.Series.objects.all()
    # serializer_class = serializer.SeriesSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializer.SeriesSerializer
        if self.action == 'retrieve':
            return serializer.SeriesDetailSerializer
        return serializer.SeriesSerializer  # create/destroy/update.

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        # search
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(title_en__icontains=query)
            ).distinct()
        # Genre
        query = self.request.GET.get("genre")
        if query is not None:
            qs = qs.filter(
                Q(seriesGenre__genre__title=query)
            ).distinct()
        # Rate
        query = self.request.GET.get("rate")
        if query is not None:
            qs = qs.filter(
                Q(rate=query)
            ).distinct()
        # Date
        query_date_from = self.request.GET.get("date_from")
        query_date_to = self.request.GET.get("date_to")
        if query_date_from is not None:
            qs = qs.filter(
                Q(created_on__gte=query_date_from)
            ).distinct()
        if query_date_to is not None:
            qs = qs.filter(
                Q(created_on__lte=query_date_to)
            ).distinct()
        # if query_date_from is not None and query_date_to is not None:
        #     qs = qs.filter(
        #         Q(created_on__range=[query_date_from, query_date_to])
        #     ).distinct()
        return qs


class SeasonViewset(viewsets.ModelViewSet):
    queryset = models.Season.objects.all()
    serializer_class = serializer.SeasonSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class EpisodeViewset(viewsets.ModelViewSet):
    queryset = models.Episode.objects.all()
    serializer_class = serializer.EpisodeSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesGenreViewset(viewsets.ModelViewSet):
    queryset = models.SeriesGenre.objects.all()
    serializer_class = serializer.SeriesGenreSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesPosterViewset(viewsets.ModelViewSet):
    queryset = models.SeriesPoster.objects.all()
    serializer_class = serializer.SeriesPosterSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesTrailerViewset(viewsets.ModelViewSet):
    queryset = models.SeriesTrailer.objects.all()
    serializer_class = serializer.SeriesTrailerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesCommentViewset(viewsets.ModelViewSet):
    queryset = models.SeriesComment.objects.all()
    serializer_class = serializer.SeriesCommentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesCastViewset(viewsets.ModelViewSet):
    queryset = models.SeriesCast.objects.all()
    serializer_class = serializer.SeriesCastSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class SeriesReviewViewset(viewsets.ModelViewSet):
    queryset = models.SeriesReview.objects.all()
    serializer_class = serializer.SeriesReviewSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class ArticleViewset(viewsets.ModelViewSet):
    queryset = models.Article.objects.all()
    serializer_class = serializer.ArticleSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class ArticleTagViewset(viewsets.ModelViewSet):
    queryset = models.ArticleTag.objects.all()
    serializer_class = serializer.ArticleTagSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class ArticleCommentViewset(viewsets.ModelViewSet):
    queryset = models.ArticleComment.objects.all()
    serializer_class = serializer.ArticleCommentSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class UserFavoriteViewset(viewsets.ModelViewSet):
    queryset = models.UserFavorite.objects.all()
    serializer_class = serializer.UserFavoriteSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


class UserRateViewset(viewsets.ModelViewSet):
    queryset = models.UserRate.objects.all()
    serializer_class = serializer.UserRateSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs


# class RelativeTypeViewset(viewsets.ModelViewSet):
#     queryset = models.RelativeType.objects.all()
#     serializer_class = serializer.RelativeTypeSerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
#
#     def get_queryset(self):
#         qs = super().get_queryset().order_by('-created_on')
#         query = self.request.GET.get("q")
#         if query is not None:
#             qs = qs.filter(
#                 Q(title__icontains=query)
#             ).distinct()
#         return qs
#
#
# class PatientProfileViewset(viewsets.ModelViewSet):
#     queryset = models.PatientProfile.objects.all()
#     serializer_class = serializer.PatientProfileSerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
#
#     def get_queryset(self):
#         qs = super().get_queryset().order_by('-created_on')
#         query = self.request.GET.get("q")
#         if query is not None:
#             qs = qs.filter(
#                 Q(user__username__icontains=query)
#             ).distinct()
#         return qs
