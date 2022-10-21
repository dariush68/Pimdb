from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

# Create your models here.


def trunc(str, num):
    return (str[:num]) if len(str) > num else str


def generate_thumbnail(obj):
    print(obj)
    if obj.image:
        image = Image.open(obj.image)
        image.thumbnail((200, 160), Image.ANTIALIAS)
        thumb_name, thumb_extension = os.path.splitext(obj.image.name)
        thumb_extension = thumb_extension.lower()
        thumb_filename = thumb_name + '_thumb' + thumb_extension
        print(thumb_extension)
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            print('foramt exit')
            FTYPE = 'JPEG'
            # return False    # Unrecognized file type
        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        try:
            image.save(temp_thumb, FTYPE)
            temp_thumb.seek(0)

            # set save=False, otherwise it will run in an infinite loop
            obj.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

            # actor.save()
        except:
            print(f'execption on {thumb_filename}')


class Country(models.Model):
    title = models.CharField(max_length=200, help_text="کشور")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='کشور انگلیسی')

    def __str__(self):
        return f'{self.title}'


class City(models.Model):
    title = models.CharField(max_length=200, help_text="شهر")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='شهر انگلیسی')

    def __str__(self):
        return f'{self.title}'


class Genre(models.Model):
    title = models.CharField(max_length=250, help_text='ژانر')
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='ژانر انگلیسی')

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    title = models.CharField(max_length=250, help_text="تگ")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='تگ انگلیسی')

    def __str__(self):
        return f'{self.title}'


class Movie(models.Model):
    title = models.CharField(max_length=500, help_text="نام فیلم")
    title_en = models.CharField(max_length=500, null=True, blank=True, help_text="نام انگلیسی فیلم")
    image = models.ImageField(upload_to="posters", null=True, blank=True, help_text="پوستر فیلم")
    thumbnail = models.ImageField(upload_to="posters/thumbnail", null=True, blank=True, help_text="پوستر انگشتی فیلم")
    duration = models.DurationField(null=True, blank=True, help_text="مدت زمان فیلم")
    created_on = models.DateField(null=True, blank=True, help_text="تاریخ تولید")
    rate = models.FloatField(default=0, help_text="امتیاز فیلم")
    abstract = models.TextField(null=True, blank=True, help_text="توضیحات مختصر")
    description = models.TextField(null=True, blank=True,help_text="توضیحات")
    view_count = models.IntegerField(default=0, help_text="تعداد بازدید")
    download_count = models.IntegerField(default=0, help_text="تعداد دانلود برای تخمین محبوبیت")
    isApproved = models.BooleanField(default=False, help_text='تایید شده توسط ادمین')

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class MovieGenre(models.Model):
    genre = models.ForeignKey(Genre, related_name="movieGenre", on_delete=models.CASCADE, help_text="زانر فیلم")
    movie = models.ForeignKey(Movie, related_name="movieGenre", on_delete=models.CASCADE, help_text="فیلم")

    def __str__(self):
        return f'{self.movie.title} - {self.genre.title}'


class MovieCountry(models.Model):
    country = models.ForeignKey(Country, related_name="movieCountries", on_delete=models.CASCADE, help_text="کشور ساخت")
    movie = models.ForeignKey(Movie, related_name="movieCountries", on_delete=models.CASCADE, help_text="فیلم")

    def __str__(self):
        return f'{self.movie.title} - {self.country.title}'


class MovieTag(models.Model):
    tag = models.ForeignKey(Tag, related_name="movieTags", on_delete=models.CASCADE, help_text="تگ فیلم")
    movie = models.ForeignKey(Movie, related_name="movieTags", on_delete=models.CASCADE, help_text="فیلم")

    def __str__(self):
        return f'{self.movie.title} - {self.tag.title}'


class MoviePoster(models.Model):
    movie = models.ForeignKey(Movie, related_name="moviePoster", on_delete=models.CASCADE, help_text="فیلم")
    title = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان')
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان انگلیسی')
    image = models.ImageField(upload_to="posters", help_text="پوستر فیلم")
    thumbnail = models.ImageField(upload_to="posters/thumbnail", null=True, blank=True, help_text="پوستر انگشتی فیلم")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(MoviePoster, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.movie.title}'


class MovieTrailer(models.Model):
    movie = models.ForeignKey(Movie, related_name="movieTrailer", on_delete=models.CASCADE, help_text="فیلم")
    title = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان')
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان انگلیسی')
    trailer = models.FileField(upload_to="trailers", null=True, blank=True, help_text="تریلر فیلم")
    image = models.ImageField(upload_to="trailers/image", null=True, blank=True, help_text="پوستر فیلم")
    thumbnail = models.ImageField(upload_to="trailers/thumbnail", null=True, blank=True, help_text="پوستر انگشتی فیلم")
    external_url = models.CharField(max_length=500, null=True, blank=True, help_text='لینک ویدیو (برای آپارات اشتراک-لینک امبد-iframe- بخش src برداشته شود)')
    duration = models.DurationField(help_text="مدت زمان")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(MovieTrailer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.movie.title}'


class Actor(models.Model):
    SEX = (
        (1, 'men'),
        (2, 'women')
    )
    country = models.ForeignKey(Country, null=True, blank=True, related_name="actors", on_delete=models.CASCADE, help_text="کشور")
    city = models.ForeignKey(City, null=True, blank=True, related_name="actors", on_delete=models.CASCADE, help_text="شهر")
    name = models.CharField(max_length=500, help_text="نام بازیگر")
    name_en = models.CharField(max_length=250, null=True, blank=True, help_text='نام انگلیسی')
    family = models.CharField(max_length=500, help_text="نام خانوادگی بازیگر")
    family_en = models.CharField(max_length=250, null=True, blank=True, help_text='نام خانوادگی انگلیسی')
    image = models.ImageField(upload_to="actors", null=True, blank=True, help_text="تصویر بازیگر")
    thumbnail = models.ImageField(upload_to="actors/thumbnail", null=True, blank=True, help_text="تصویر انگشتی بازیگر")
    birthDay = models.DateField(null=True, blank=True, help_text="تاریخ تولد")
    bio = models.TextField(help_text="بیوگرافی", null=True, blank=True)
    bio_short = models.TextField(help_text="خلاصه بیوگرافی", null=True, blank=True)
    bio_en = models.CharField(max_length=250, null=True, blank=True, help_text='بیوگرافی انگلیسی')
    isApproved = models.BooleanField(default=False, help_text='تایید شده توسط ادمین')
    sex = models.SmallIntegerField(choices=SEX, null=True, blank=True, default=1, help_text="جنسیت")
    view_count = models.IntegerField(default=0, help_text="تعداد بازدید")
    download_count = models.IntegerField(default=0, help_text="تعداد دانلود برای تخمین محبوبیت")
    # TODO: generate seperate model for user seen actor for estimate view and popularity and intelligent recommend system

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(Actor, self).save(*args, **kwargs)

    def get_fullName(self):
        return f'{self.name} {self.family}'

    def __str__(self):
        return f'{self.name} {self.family}'


class ActorMoviePoster(models.Model):
    moviePoster = models.ForeignKey(MoviePoster, related_name="actorMoviePosters", on_delete=models.CASCADE,
                                    help_text="پوستر فیلم")
    actor = models.ForeignKey(Actor, related_name="actorMoviePosters", on_delete=models.CASCADE, help_text="بازیگر مرتبط")

    def __str__(self):
        return f'{self.moviePoster.title} - {self.actor.name} {self.actor.family}'


class ActorMovieTrailer(models.Model):
    movieTrailer = models.ForeignKey(MovieTrailer, related_name="actorMovieTrailers", on_delete=models.CASCADE,
                                    help_text="تریلر فیلم")
    actor = models.ForeignKey(Actor, related_name="actorMovieTrailers", on_delete=models.CASCADE, help_text="بازیگر مرتبط")

    def __str__(self):
        return f'{self.movieTrailer.title} - {self.actor.name} {self.actor.family}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="کاربر")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")
    message = models.TextField(help_text="پیام")
    rate = models.FloatField(help_text="امتیاز فیلم")

    def __str__(self):
        return f'{self.user} - {self.message}'


class MovieComment(models.Model):
    movie = models.ForeignKey(Movie, related_name="movieComments", on_delete=models.CASCADE, help_text="فیلم")
    comment = models.ForeignKey(Comment, related_name="movieComments", on_delete=models.CASCADE, help_text="پیام")

    def __str__(self):
        return f'{self.movie.title} - {self.comment.user}'


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="کاربر")
    title = models.CharField(max_length=300, null=True, blank=True, help_text="عنوان")
    review = models.TextField(null=True, blank=True, help_text="بازبینی")
    rate = models.FloatField(null=True, blank=True, help_text="امتیاز فیلم")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")
    isApproved = models.BooleanField(default=False, help_text='تایید شده توسط ادمین')

    def __str__(self):
        return f'{self.user} - {trunc(self.review, 100)}'


class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, related_name="movieReviews", on_delete=models.CASCADE, help_text="فیلم")
    review = models.ForeignKey(Review, related_name="movieReviews", on_delete=models.CASCADE, help_text="پیام")

    def __str__(self):
        return f'{self.movie.title} - {self.review.user}'


class Cast(models.Model):
    title = models.CharField(max_length=250, help_text="نقش عوامل")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='نقش عوامل انگلیسی')

    def __str__(self):
        return f'{self.title}'


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, related_name="movieCasts", on_delete=models.CASCADE, help_text="فیلم")
    actor = models.ForeignKey(Actor, related_name="movieCasts", on_delete=models.CASCADE, help_text="بازیگر")
    cast = models.ForeignKey(Cast, related_name="movieCasts", on_delete=models.CASCADE, help_text="عنوان وظیفه")
    role = models.CharField(max_length=250, null=True, blank=True, help_text="نقش")
    priority = models.IntegerField(default=0, help_text="اولویت نقش")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f'{self.movie.title} - {self.actor.name} - {self.cast.title} - {self.role}'


class Series(models.Model):
    title = models.CharField(max_length=500, help_text="نام سریال")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='سریال انگلیسی')
    image = models.ImageField(upload_to="posters", null=True, blank=True, help_text="پوستر فیلم")
    thumbnail = models.ImageField(upload_to="posters/thumbnail", null=True, blank=True, help_text="پوستر انگشتی سریال")
    created_on = models.DateField(null=True, blank=True,help_text="تاریخ تولید")
    rate = models.FloatField(default=0, help_text="امتیاز فیلم")
    abstract = models.TextField(null=True, blank=True, help_text="توضیحات مختصر")
    description = models.TextField(null=True, blank=True, help_text="توضیحات کامل")
    view_count = models.IntegerField(default=0, help_text="تعداد بازدید")
    download_count = models.IntegerField(default=0, help_text="تعداد دانلود برای تخمین محبوبیت")
    isApproved = models.BooleanField(default=False, help_text='تایید شده توسط ادمین')

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(Series, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class Season(models.Model):
    series = models.ForeignKey(Series, related_name="seriesSeasons", on_delete=models.CASCADE, help_text="سریال")
    number = models.IntegerField(help_text="شماره فصل سریال")
    image = models.ImageField(upload_to="posters", help_text="پوستر فصل")
    thumbnail = models.ImageField(upload_to="posters/thumbnail", help_text="پوستر انگشتی فصل")
    title = models.CharField(max_length=500, help_text="عنوان فصل")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان فصل انگلیسی')
    created_on = models.DateField(help_text="تاریخ تولید")

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(Season, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.number} - {self.series.title}'


class Episode(models.Model):
    season = models.ForeignKey(Season, related_name="seasonEpisodes", on_delete=models.CASCADE, help_text="فصل")
    number = models.IntegerField(help_text="شماره قسمت سریال")
    image = models.ImageField(upload_to="posters", help_text="پوستر فصل")
    thumbnail = models.ImageField(upload_to="posters/thumbnail", help_text="پوستر انگشتی فصل")
    duration = models.DurationField(help_text="مدت زمان")
    title = models.CharField(max_length=500, help_text="عنوان قسمت")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان قسمت انگلیسی')
    created_on = models.DateField(help_text="تاریخ تولید")

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(Episode, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.number} - {self.season.title}'


class SeriesGenre(models.Model):
    genre = models.ForeignKey(Genre, related_name="seriesGenres", on_delete=models.CASCADE, help_text="زانر سریال")
    series = models.ForeignKey(Series, related_name="seriesGenres", on_delete=models.CASCADE, help_text="سریال")

    def __str__(self):
        return f'{self.genre.title} - {self.series.title}'


class SeriesPoster(models.Model):
    series = models.ForeignKey(Series, related_name="seriesPosters", on_delete=models.CASCADE, help_text="سریال")
    image = models.ImageField(upload_to="posters", help_text="پوستر سریال")
    thumbnail = models.ImageField(upload_to="posters/thumbnail", help_text="پوستر انگشتی فصل")
    title = models.CharField(max_length=120, null=True, blank=True, help_text="عنوان فصل")
    title_en = models.CharField(max_length=120, null=True, blank=True, help_text='عنوان فصل انگلیسی')
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(SeriesPoster, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.series.title}'


class SeriesTrailer(models.Model):
    series = models.ForeignKey(Series, related_name="seriesTrailers", on_delete=models.CASCADE, help_text="سریال")
    trailer = models.FileField(upload_to="trailers", help_text="تریلر سریال")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")
    title = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان')
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان انگلیسی')
    image = models.ImageField(upload_to="trailers/image", help_text="پوستر فیلم")
    thumbnail = models.ImageField(upload_to="trailers/thumbnail", help_text="پوستر انگشتی فیلم")
    duration = models.DurationField(help_text="مدت زمان")

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(SeriesTrailer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.series.title} - {self.trailer.name}'


class SeriesComment(models.Model):
    series = models.ForeignKey(Series, related_name="seriesComments", on_delete=models.CASCADE, help_text="سریال")
    comment = models.ForeignKey(Comment, related_name="seriesComments", on_delete=models.CASCADE, help_text="پیام")

    def __str__(self):
        return f'{self.series.title}'


class SeriesCast(models.Model):
    series = models.ForeignKey(Series, related_name="seriesCasts", on_delete=models.CASCADE, help_text="سریال")
    actor = models.ForeignKey(Actor, related_name="seriesCasts", on_delete=models.CASCADE, help_text="بازیگر")
    cast = models.ForeignKey(Cast, related_name="seriesCasts", on_delete=models.CASCADE, help_text="عنوان وظیفه")
    role = models.CharField(max_length=250, null=True, blank=True, help_text="نقش")
    priority = models.IntegerField(default=0, help_text="اولویت نقش")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def __str__(self):
        return f'{self.cast.title} - {self.series.title} - {self.cast.title} - {self.role}'


class SeriesReview(models.Model):
    series = models.ForeignKey(Series, related_name="seriesReviews", on_delete=models.CASCADE, help_text="سریال")
    review = models.ForeignKey(Review, related_name="seriesReviews", on_delete=models.CASCADE, help_text="بازبینی")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def __str__(self):
        return f'{self.series.title}'


class ArticleCategory(models.Model):
    title = models.CharField(max_length=250, help_text="عنوان دسته بندی مقاله")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان دسته بندی مقاله انگلیسی')

    def __str__(self):
        return f'{self.title}'


class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, help_text="کاربر")
    series = models.ForeignKey(Series, null=True, blank=True, related_name="articles", on_delete=models.CASCADE, help_text="سریال")
    movie = models.ForeignKey(Movie, null=True, blank=True, related_name="articles", on_delete=models.CASCADE, help_text="فیلم")
    articleCategory = models.ForeignKey(ArticleCategory, related_name="articles", on_delete=models.CASCADE, help_text="دسته بندی")
    title = models.CharField(max_length=500, help_text="عنوان مقاله")
    title_en = models.CharField(max_length=250, null=True, blank=True, help_text='عنوان مقاله انگلیسی')
    abstract = models.TextField(null=True, blank=True, help_text='خلاصه مقاله')
    text = models.TextField(null=True, blank=True, help_text='متن مقاله')
    image = models.ImageField(upload_to="Article", null=True, blank=True, help_text="تصویر مقاله")
    thumbnail = models.ImageField(upload_to="Article/thumbnail", null=True, blank=True, help_text="تصویر انگشتی مقاله")
    reference = models.CharField(max_length=250, null=True, blank=True, help_text='مرجع')
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")
    isApproved = models.BooleanField(default=False, help_text='تایید شده توسط ادمین')

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        generate_thumbnail(self)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, null=True, blank=True, related_name="articleTags", on_delete=models.CASCADE, help_text="مقاله")
    tag = models.ForeignKey(Tag, null=True, blank=True, related_name="articleTags", on_delete=models.CASCADE, help_text="تگ")

    def __str__(self):
        return f'{self.tag.title} - {self.article.title}'


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, null=True, blank=True, related_name="articleComments", on_delete=models.CASCADE, help_text="مقاله")
    comment = models.ForeignKey(Comment, related_name="articleComments", on_delete=models.CASCADE, help_text="پیام")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def __str__(self):
        return f'{self.article.title}'


class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="کاربر")
    series = models.ForeignKey(Series, null=True, blank=True, related_name="userFavorites", on_delete=models.CASCADE,
                               help_text="سریال")
    movie = models.ForeignKey(Movie, null=True, blank=True, related_name="userFavorites", on_delete=models.CASCADE,
                              help_text="فیلم")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")

    def __str__(self):
        return f'{self.series.title if self.series else ""} - {self.movie.title if self.movie else ""}'


class UserRate(models.Model):
    STAR_CONVERSION = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
        (6, 'Six'),
        (7, 'Seven'),
        (8, 'Eight'),
        (9, 'Nine'),
        (10, 'ten'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="کاربر")
    series = models.ForeignKey(Series, null=True, blank=True, related_name="userRates", on_delete=models.CASCADE,
                               help_text="سریال")
    movie = models.ForeignKey(Movie, null=True, blank=True, related_name="userRates", on_delete=models.CASCADE,
                              help_text="فیلم")
    created_on = models.DateField(auto_now_add=True, help_text="تاریخ ایجاد")
    rate = models.PositiveSmallIntegerField(choices=STAR_CONVERSION, help_text="امتیاز فیلم")

    def __str__(self):
        return f'{self.rate} - {self.series.title if self.series else ""} - {self.movie.title if self.movie else ""}'


class MovieInTheatre(models.Model):
    movie = models.ForeignKey(Movie, related_name="movieInTheatres", on_delete=models.CASCADE, help_text="فیلم در حال اکران")
    created_on = models.DateField(null=True, blank=True, help_text="تاریخ شروع اکران")
    end_on = models.DateField(null=True, blank=True, help_text="تاریخ اتمام اکران")
    ticket_url = models.CharField(max_length=500, null=True, blank=True, help_text="لینک بلیط")

    def __str__(self):
        return f'{self.movie.title}'


class SpoliightActor(models.Model):
    actor = models.ForeignKey(Actor, related_name="spoliightActors", on_delete=models.CASCADE, help_text="بازیگر مرتبط")
    is_show = models.BooleanField(default=False, help_text='نمایش')


class SpoliightMovie(models.Model):
    movie = models.ForeignKey(Movie, related_name="spoliightMovies", on_delete=models.CASCADE, help_text="فیلم در حال اکران")
    is_show = models.BooleanField(default=False, help_text='نمایش')

    def __str__(self):
        return f'{self.movie.title}'
