import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from urllib.request import urlopen
import json

import jdatetime
import timeit
import requests
from bs4 import BeautifulSoup
from django.core.files import File
from django.db.models import Q

import os.path
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


from Core import models


def valid_img(img):
    """Verifies that an instance of a PIL Image Class is actually an image and returns either True or False."""
    type = img.format
    if type in ('GIF', 'JPEG', 'JPG', 'PNG'):
        try:
            img.verify()
            return True
        except:
            return False
    else:
        return False


def get_instrument(sites):
    """ return candel info for selected instrument"""
    with requests.get(sites) as request:
        page = request
        # print(page.text)
        print(page)

        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())

        # list of actors
        d1 = soup.find_all('div', class_='list-item')
        itm = d1[0]
        for itm in d1:
            a1 = itm.find('a')
            if a1.has_attr('href'):
                print('==============================')
                print(a1['href'])

                page2 = requests.get(a1['href'])
                soup2 = BeautifulSoup(page2.text, 'html.parser')
                # bio = soup2.xpath('//*[@id="mw-content-text"]/div[1]/p[2]')

                div = soup2.find(id='main-page-part')
                image_url = div.select_one('div:nth-child(1) > div.right-col > img')['src']
                # img = Image.open(requests.get(image_url, stream=True).raw)
                # name_fa = div.select_one('div:nth-child(1) > div.right-col > img')['alt']

                name_h = div.select_one('div:nth-child(1) > div.left-col.flex-wrap-col > div.info-top.relative > h1')
                t = name_h.text.split("\u200f")
                name_fa = t[1]
                name_en = t[2]
                print(name_fa, ' => ', sites)
                name = name_fa.split(" ")[0]
                family = name_fa.split(" ")[1]

                short_bio = div.select_one('div:nth-child(1) > div.left-col.flex-wrap-col > div:nth-child(3)').text

                res = models.Actor.objects.filter(Q(name=name) & Q(family=family))  # .first()
                if len(res) > 0:
                    act = res.first()
                    act.bio_short = short_bio
                    act.save()
                    print("--exist")
                    continue

                birthday_temp = div.select_one(
                    'div:nth-child(1) > div.left-col.flex-wrap-col > div.underline-links.maznoom-d > div')
                if birthday_temp is not None:
                    bd = birthday_temp.text.split(" ")[1]
                    if len(bd.split('/')) > 2:
                        t_year = (bd.split('/')[0])
                        t_month = (bd.split('/')[1])
                        t_day = (bd.split('/')[2])
                        if t_year.isdigit() and t_month.isdigit() and t_day.isdigit():
                            year = int(bd.split('/')[0])
                            month = int(bd.split('/')[1])
                            day = int(bd.split('/')[2])
                            if year < 1500:
                                birthday_gregorian_date = jdatetime.date(year, month, day).togregorian()
                                # jalili_date =  jdatetime.date.fromgregorian(day=19,month=5,year=2017)

                            else:
                                birthday_gregorian_date = year + "-" + month + "-" + day
                        else:
                            birthday_temp = None
                    else:
                        birthday_temp = None

                t = soup2.select_one('#page-info > div.text.padded')
                bio = ""
                if t is not None:
                    bio = t.text
                # for itm in t:
                #     print(itm)

                # country = models.Country.objects.first()
                # city = models.City.objects.first()
                c = models.Actor.objects.create(
                    # country=country,
                    # city=city,
                    name=name_fa.split(" ")[0],
                    family=name_fa.split(" ")[1],
                    bio=bio
                )
                # birthDay=birthday.replace('/','-').replace('/','-').replace('/','-'),

                if name_en is not None:
                    if len(name_en.split(" ")) > 1:
                        c.name_en = name_en.split(" ")[0]
                        c.family_en = name_en.split(" ")[1]

                if birthday_temp is not None:
                    c.birthDay = birthday_gregorian_date

                # Save image
                img_temp = tempfile.NamedTemporaryFile()
                img_temp.write(urlopen(image_url).read())
                img_temp.flush()
                c.image.save("%s.jpg" % name_en, File(img_temp))
                c.thumbnail.save("%s_tb.jpg" % name_en, File(img_temp))
                c.save()


def get_movie(sites):
    """ return candel info for selected instrument"""
    with requests.get(sites) as request:
        # sites = "https://www.manzoom.ir/name/?p=1"
        # request = requests.get(sites)

        page = request
        # print(page.text)
        print(page)

        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())

        # list of actors
        d1 = soup.find_all('div', class_='list-item')
        itm = d1[0]
        for itm in d1:
            a1 = itm.find('a')
            if a1.has_attr('href'):
                print('==============================')
                print(a1['href'])

                page2 = requests.get(a1['href'])
                soup2 = BeautifulSoup(page2.text, 'html.parser')
                # bio = soup2.xpath('//*[@id="mw-content-text"]/div[1]/p[2]')

                div = soup2.find(id='main-page-part')
                image_url = div.select_one('div:nth-child(1) > div.right-col > img')['src']

                name_h = div.select_one('div:nth-child(1) > div.left-col.flex-wrap-col > div.info-top.relative > h1')
                t = name_h.text.split("\u200f")
                name_fa = t[1]
                name_en = t[2]
                print(name_fa, ' => ', sites)
                name = name_fa.split(" ")[0]
                family = name_fa.split(" ")[1]

                div_movies = soup2.find_all('div', class_='person-movie-row')
                print('------------ ', len(div_movies))

                res = models.Actor.objects.filter(Q(name=name) & Q(family=family))  # .first()
                if len(res) > 0:
                    actor = res.first()
                    for movie in div_movies:
                        # movie = div_movies[2]
                        link = movie.find('a')['href']
                        print("--movie ", movie.text)
                        is_movie = True

                        # print(movie.text.index('سریال تلویزیونی'))
                        if movie.text.find('سریال تلویزیونی') > -1:
                            is_movie = False
                        if movie.text.find('تئاتر') > -1:
                            is_movie = False

                        print('movie: ', is_movie)
                        page_movie = requests.get(link)
                        soup_movie = BeautifulSoup(page_movie.text, 'html.parser')
                        movie_date = None

                        if is_movie:
                            txt = soup_movie.find('div', class_='info-top-header').text
                            temp_list = txt.split('(')
                            title = temp_list[0].strip()
                            temp_list = temp_list[1].split(' ')
                            t_year = temp_list[0].replace('(', '').replace(')', '').strip()
                            title_en = ''
                            if len(temp_list) > 1:
                                temp_list.pop(0)
                                title_en = " ".join(temp_list).replace('\u200f', '')
                            if t_year.isdigit():
                                year = int(t_year)
                                if year < 1500:
                                    movie_date = jdatetime.date(year, 1, 1).togregorian()
                                else:
                                    movie_date = year + '-01-01'

                            # c_gener = soup_movie.select_one('#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div.info-top.relative > div.flex-row.maznoom-d.m-t-1 > div:nth-child(2) > span').text
                            info_list = soup_movie.find_all('div', class_='short-info')
                            c_duration = None
                            c_gener = None
                            if len(info_list) > 1:
                                if info_list[1].text.find('دقیقه') > -1:
                                    print(info_list[1].text.find('دقیقه'))
                                    c_duration = info_list[1].text.split(' ')[0]
                                    if c_duration.isdigit():
                                        c_duration = timedelta(minutes=int(c_duration))
                                    if len(info_list) > 2:
                                        c_gener = info_list[2].text
                                else:
                                    c_gener = info_list[1].text

                            generList = []
                            if c_gener:
                                generList = c_gener.split(',')

                            c_abstract = soup_movie.select_one(
                                '#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div:nth-child(5)').text
                            c_description = soup_movie.select_one('#page-info > div.text > p:nth-child(1)').text

                            image_url = \
                            soup_movie.select_one('#main-page-part > div:nth-child(1) > div.right-col > img')['src']

                            print(movie_date, title)
                            obj, created = models.Movie.objects.get_or_create(
                                title=title,
                                title_en=title_en,
                                created_on=movie_date,
                                abstract=c_abstract,
                                description=c_description
                            )

                            if c_duration:
                                obj.duration = c_duration
                            # ignore existed movie
                            # if created is False:
                            #     continue

                            # Save image
                            img_temp = tempfile.NamedTemporaryFile()
                            img_temp.write(urlopen(image_url).read())
                            img_temp.flush()
                            obj.image.save("%s.jpg" % title, File(img_temp))
                            obj.thumbnail.save("%s_tb.jpg" % title, File(img_temp))
                            obj.save()

                            for gener in generList:
                                gener = gener.strip()
                                obj_genre, c_genre = models.Genre.objects.get_or_create(title=gener)
                                obj_movie_genre, c_movie_genre = models.MovieGenre.objects.get_or_create(
                                    genre=obj_genre, movie=obj)

                            # MovieGenre
                            # MoviePoster
                            # MovieTrailer
                            # MovieCast

                    print("--exist ")
                    # continue
                # break


def get_movie_direct(movie, index):
    if movie['type'] != 'Movie':
        print(f"-- ignore {movie['title']}")
        return
    print(f"{index} -- start scrap {movie['title']}")

    with requests.get(movie['href']) as request:
        # sites = "https://www.manzoom.ir/name/?p=1"
        # request = requests.get(sites[0]['href'])

        page = request
        # print(page.text)
        # print(page)

        soup_movie = BeautifulSoup(page.text, 'html.parser')

        txt = soup_movie.find('div', class_='info-top-header').text
        temp_list = txt.split('(')
        title = temp_list[0].strip()
        temp_list = temp_list[1].split(' ')
        t_year = temp_list[0].replace('(', '').replace(')', '').strip()
        title_en = ''
        if len(temp_list) > 1:
            temp_list.pop(0)
            title_en = " ".join(temp_list).replace('\u200f', '')
        if t_year.isdigit():
            year = int(t_year)
            if year < 1500:
                movie_date = jdatetime.date(year, 1, 1).togregorian()
            else:
                movie_date = year + '-01-01'

        # c_gener = soup_movie.select_one('#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div.info-top.relative > div.flex-row.maznoom-d.m-t-1 > div:nth-child(2) > span').text
        info_list = soup_movie.find_all('div', class_='short-info')
        c_duration = None
        c_gener = None
        if len(info_list) > 1:
            if info_list[1].text.find('دقیقه') > -1:
                # print(info_list[1].text.find('دقیقه'))
                c_duration = info_list[1].text.split(' ')[0]
                if c_duration.isdigit():
                    c_duration = timedelta(minutes=int(c_duration))
                if len(info_list) > 2:
                    c_gener = info_list[2].text
            else:
                c_gener = info_list[1].text

        generList = []
        if c_gener:
            generList = c_gener.split(',')

        c_abstract = soup_movie.select_one(
            '#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div:nth-child(5)').text
        c_description = soup_movie.select_one('#page-info > div.text > p:nth-child(1)').text

        image_url = \
        soup_movie.select_one('#main-page-part > div:nth-child(1) > div.right-col > img')['src']

        # print(movie_date, title)
        obj, created = models.Movie.objects.get_or_create(
            title=title,
            title_en=title_en,
            created_on=movie_date,
            abstract=c_abstract,
            description=c_description
        )

        if c_duration:
            obj.duration = c_duration
        # ignore existed movie
        # if created is False:
        #     continue

        # Save image
        if image_url.find('No-Poster.jpg') == -1:
            img_temp = tempfile.NamedTemporaryFile()
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            obj.image.save("%s.jpg" % title, File(img_temp))
        # obj.thumbnail.save("%s_tb.jpg" % title, File(img_temp))
        obj.save()

        for gener in generList:
            gener = gener.strip()
            obj_genre, c_genre = models.Genre.objects.get_or_create(title=gener)
            obj_movie_genre, c_movie_genre = models.MovieGenre.objects.get_or_create(
                genre=obj_genre, movie=obj)

        # MovieGenre
        # MoviePoster
        # MovieTrailer
        # MovieCast


def get_cast_direct(cast, index):
    if cast['type'] == 'Theatre':
        print(f"-- ignore {cast['title']}")
        return
    print(f"{index} -- start scrap {cast['title']}")

    with requests.get(cast['href']) as request:
        # sites = "https://www.manzoom.ir/name/?p=1"
        # request = requests.get(sites[0]['href'])

        page = request
        # print(page.text)
        # print(page)

        soup_movie = BeautifulSoup(page.text, 'html.parser')

        container = soup_movie.select_one('#main > div.right-part.right > div.row > div > div.slide-container.dual-row.hover-links')


cast_list = []


def get_cast_link(movie, index):

    print(f"{index} -- start scrap {movie['title']}")

    with requests.get(movie['href']) as request:
        # sites = "https://www.manzoom.ir/name/?p=1"
        # request = requests.get(sites[0]['href'])

        page = request
        soup_movie = BeautifulSoup(page.text, 'html.parser')

        txt = soup_movie.find('div', class_='info-top-header').text
        temp_list = txt.split('(')
        title = temp_list[0].strip()
        cast_link = soup_movie.select_one('#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div.underline-links.maznoom-d > div:nth-child(3) > a')['href']
        cast_list.append({
            'title': title,
            'type': movie['type'],
            'href': cast_link
        })


def get_series_direct(movie, index):
    # print(f"*** {index} -- check type {movie['type']}")
    # return
    if movie['type'] != 'Serial':
        # print(f"-- ignore {movie['title']}")
        return
    print(f"{index} -- start scrap {movie['title']}")

    with requests.get(movie['href']) as request:
        # sites = "https://www.manzoom.ir/name/?p=1"
        # request = requests.get(sites[0]['href'])

        page = request
        # print(page.text)
        # print(page)

        soup_movie = BeautifulSoup(page.text, 'html.parser')

        txt = soup_movie.find('div', class_='info-top-header').text
        temp_list = txt.split('(')
        title = temp_list[0].strip()
        temp_list = temp_list[1].split(' ')
        t_year = temp_list[0].replace('(', '').replace(')', '').strip()
        title_en = ''
        if len(temp_list) > 1:
            temp_list.pop(0)
            title_en = " ".join(temp_list).replace('\u200f', '')
        if t_year.isdigit():
            year = int(t_year)

            if year < 1500:
                movie_date = jdatetime.date(year, 1, 1).togregorian()
            else:
                movie_date = year + '-01-01'

        # c_gener = soup_movie.select_one('#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div.info-top.relative > div.flex-row.maznoom-d.m-t-1 > div:nth-child(2) > span').text
        info_list = soup_movie.find_all('div', class_='short-info')
        c_duration = None
        c_gener = None
        if len(info_list) > 1:
            c_gener = info_list[1].text

        generList = []
        if c_gener:
            generList = c_gener.split(',')

        c_abstract = soup_movie.select_one(
            '#main-page-part > div:nth-child(1) > div.left-col.flex-wrap-col > div:nth-child(5)').text
        c_description = soup_movie.select_one('#page-info > div.text > p:nth-child(1)').text

        image_url = \
        soup_movie.select_one('#main-page-part > div:nth-child(1) > div.right-col > img')['src']

        # print(movie_date, title)
        obj, created = models.Series.objects.get_or_create(
            title=title,
            title_en=title_en,
            created_on=movie_date,
            abstract=c_abstract,
            description=c_description
        )

        # Save image
        if image_url.find('No-Poster.jpg') == -1:
            img_temp = tempfile.NamedTemporaryFile()
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            obj.image.save("%s.jpg" % title, File(img_temp))
        # obj.thumbnail.save("%s_tb.jpg" % title, File(img_temp))
        obj.save()

        for gener in generList:
            gener = gener.strip()
            obj_genre, c_genre = models.Genre.objects.get_or_create(title=gener)
            obj_series_genre, c_movie_genre = models.SeriesGenre.objects.get_or_create(
                genre=obj_genre, series=obj)

        # MovieGenre
        # MoviePoster
        # MovieTrailer
        # MovieCast


movie_list = []


def get_movie_list(actor):
    print(f"start scrap {actor['actor']}")
    # actor = {"actor": "\u0622\u062a\u0634 \u062a\u0642\u06cc\u200c\u067e\u0648\u0631", "href": "https://www.manzoom.ir/name/nm0257941/%D8%A2%D8%AA%D8%B4-%D8%AA%D9%82%DB%8C%E2%80%8C%D9%BE%D9%88%D8%B1"}
    with requests.get(actor['href']) as request:
        # request = requests.get(actor['href'])

        page = request
        # print(page.text)
        # print(page)

        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())

        # list of movies
        div_movies = soup.find_all('div', class_='person-movie-row')
        # print('------------ ', len(div_movies))

        for movie in div_movies:
            # movie = div_movies[2]
            link = movie.find('a')['href']
            # print("--movie ", movie.text)
            type = ''

            # print(movie.text.index('سریال تلویزیونی'))
            if movie.text.find('سریال تلویزیونی') > -1:
                # print('--- its Serial ---')
                type = 'Serial'
            elif movie.text.find('تئاتر') > -1:
                # print('--- its Theatre ---')
                type = 'Theatre'
            else:
                # print('--- its Movie ---')
                type = 'Movie'

            movie_list.append({
                'title': movie.text,
                'type': type,
                'href': link,
            })


actor_list = []


def get_actor_list(sites):
    print(f'start scrap {sites}')
    with requests.get(sites) as request:
        # sites = "https://www.manzoom.ir/name/?p=1"
        # request = requests.get(sites)

        page = request
        # print(page.text)
        print(page)

        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup.prettify())

        # list of actors
        d1 = soup.find_all('div', class_='list-item')
        # itm = d1[0]
        for itm in d1:
            a1 = itm.find('a')
            name = itm.find('div', class_='right').find('a').text
            if a1.has_attr('href'):
                # print('==============================')
                # print(name, a1['href'])
                actor_list.append({
                    'actor': name,
                    'href': a1['href']
                })


def scrapp_actor(page=1):
    # url = f'https://www.manzoom.ir/iranian-artist/biography/?p={page}'
    url = f'https://www.manzoom.ir/name/?p={page}'
    page = requests.get(url)
    # print(page.text)
    print(page)

    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup.prettify())

    # list of actors
    d1 = soup.find_all('div', class_='list-item')
    itm = d1[0]
    for itm in d1:
        a1 = itm.find('a')
        if a1.has_attr('href'):
            print('==============================')
            print(a1['href'])

            page2 = requests.get(a1['href'])
            soup2 = BeautifulSoup(page2.text, 'html.parser')
            # bio = soup2.xpath('//*[@id="mw-content-text"]/div[1]/p[2]')

            div = soup2.find(id='main-page-part')
            image_url = div.select_one('div:nth-child(1) > div.right-col > img')['src']
            # img = Image.open(requests.get(image_url, stream=True).raw)
            # name_fa = div.select_one('div:nth-child(1) > div.right-col > img')['alt']

            name_h = div.select_one('div:nth-child(1) > div.left-col.flex-wrap-col > div.info-top.relative > h1')
            t = name_h.text.split("\u200f")
            name_fa = t[1]
            name_en = t[2]
            print(name_fa)
            name = name_fa.split(" ")[0]
            family = name_fa.split(" ")[1]

            short_bio = div.select_one('div:nth-child(1) > div.left-col.flex-wrap-col > div:nth-child(3)').text

            res = models.Actor.objects.filter(Q(name=name) & Q(family=family)).first()
            if len(res) > 0:
                res.bio_short = short_bio
                res.save()
                print("--exist")
                continue

            birthday_temp = div.select_one(
                'div:nth-child(1) > div.left-col.flex-wrap-col > div.underline-links.maznoom-d > div')
            if birthday_temp is not None:
                bd = birthday_temp.text.split(" ")[1]
                if len(bd.split('/')) > 2:
                    t_year = (bd.split('/')[0])
                    t_month = (bd.split('/')[1])
                    t_day = (bd.split('/')[2])
                    if t_year.isdigit() and t_month.isdigit() and t_day.isdigit():
                        year = int(bd.split('/')[0])
                        month = int(bd.split('/')[1])
                        day = int(bd.split('/')[2])
                        if year < 1500:
                            birthday_gregorian_date = jdatetime.date(year, month, day).togregorian()
                            # jalili_date =  jdatetime.date.fromgregorian(day=19,month=5,year=2017)
                        else:
                            birthday_gregorian_date = year + '-' + month + '-' + day
                    else:
                        birthday_temp = None
                else:
                    birthday_temp = None

            t = soup2.select_one('#page-info > div.text.padded')
            bio = ""
            if t is not None:
                bio = t.text
            # for itm in t:
            #     print(itm)

            # country = models.Country.objects.first()
            # city = models.City.objects.first()
            c = models.Actor.objects.create(
                # country=country,
                # city=city,
                name=name_fa.split(" ")[0],
                family=name_fa.split(" ")[1],
                bio=bio
            )
            # birthDay=birthday.replace('/','-').replace('/','-').replace('/','-'),

            if name_en is not None:
                if len(name_en.split(" ")) > 1:
                    c.name_en = name_en.split(" ")[0]
                    c.family_en = name_en.split(" ")[1]

            if birthday_temp is not None:
                c.birthDay = birthday_gregorian_date

            # Save image
            img_temp = tempfile.NamedTemporaryFile()
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            c.image.save("%s.jpg" % name_en, File(img_temp))
            c.thumbnail.save("%s_tb.jpg" % name_en, File(img_temp))
            c.save()


def scrapp():
    print('run scrap manzoom')
    pass


def read_json():
    # Opening JSON file
    f = open('movie_list.json', )

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    seen = set()
    new_l = []
    for d in data:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_l.append(d)

    res = []
    for i in data:
        if i not in res:
            res.append(i)

    # Iterating through the json
    # list
    # for i in data:
    #     print(i)

    # Closing file
    f.close()

    with open('movie_list.json', 'w') as fp:
        json.dump(new_l, fp)


def scrap_thread():
    num_of_threads = 10
    sites = []

    for i in range(88):
        sites.append(f'https://www.manzoom.ir/name/?p={i + 2}')

    # with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
    #     pool.map(get_instrument, sites)

    with ThreadPoolExecutor(max_workers=num_of_threads) as pool:
        pool.map(get_movie, sites)

    # for i in range(87, 88): # 87
    #     print(i)
    #     scrapp_actor(i)


def scrap_movie_list():
    num_of_threads = 20
    sites = []

    for i in range(87):  # 87
        sites.append(f'https://www.manzoom.ir/name/?p={i + 1}')

    print('start scrap actor list ...')
    start = timeit.default_timer()

    with ThreadPoolExecutor(max_workers=min(num_of_threads, len(sites))) as pool:
        pool.map(get_actor_list, sites)

    time_scrap = timeit.default_timer()
    print('Time scrap: ', time_scrap - start)

    print(f'len of actors: {len(actor_list)}')

    with open('actor_list.json', 'w') as fp:
        json.dump(actor_list, fp)

    time_save = timeit.default_timer()
    print('Time save: ', time_save - time_scrap)

    # ======================================================
    # scrap movie list
    print('start scrap movie list ...')

    with ThreadPoolExecutor(max_workers=min(num_of_threads, len(actor_list))) as pool:
        pool.map(get_movie_list, actor_list)

    time_scrap_movie = timeit.default_timer()
    print('Time scrap movie: ', time_scrap_movie - time_save)

    print(f'len of movies: {len(movie_list)}') # 50970

    seen = set()
    new_movie_list = []
    for d in movie_list:
        t = tuple(d.items())
        if t not in seen:
            seen.add(t)
            new_movie_list.append(d)

    print(f'len of movies after remove redundancy: {len(new_movie_list)}') # 6124

    with open('movie_list.json', 'w') as fp:
        json.dump(new_movie_list, fp)

    time_save_movie = timeit.default_timer()
    print('Time save movie: ', time_save_movie - time_scrap_movie)


def scrap_movie_thread():
    num_of_threads = 20
    sites = []

    # Opening JSON file
    f = open('movie_list.json', )
    data = json.load(f)
    f.close()

    sites = data#[:1]
    index = list(range(0, len(sites)))

    print('start scrap movies ...')
    start = timeit.default_timer()

    # fetch movie
    # with ThreadPoolExecutor(max_workers=min(num_of_threads, len(sites))) as pool:
    #     pool.map(get_movie_direct, sites, index)

    # fetch series
    with ThreadPoolExecutor(max_workers=min(num_of_threads, len(sites))) as pool:
        pool.map(get_series_direct, sites, index)

    time_scrap = timeit.default_timer()
    print('Time scrap: ', time_scrap - start)

    print(f'len of actors: {len(actor_list)}')


def scrap_cast_list():
    num_of_threads = 20
    sites = []

    # Opening JSON file
    f = open('movie_list.json', )
    data = json.load(f)
    f.close()

    sites = data#[:1]
    index = list(range(0, len(sites)))

    print('start scrap movies ...')
    start = timeit.default_timer()

    # fetch series
    with ThreadPoolExecutor(max_workers=min(num_of_threads, len(sites))) as pool:
        pool.map(get_cast_link, sites, index)

    time_scrap = timeit.default_timer()
    print('Time scrap: ', time_scrap - start)

    print(f'len of cast list: {len(cast_list)}')

    with open('cast_list.json', 'w') as fp:
        json.dump(cast_list, fp)

    time_save_cast = timeit.default_timer()
    print('Time save movie: ', time_save_cast - time_scrap)


def scrap_cast_thread():
    num_of_threads = 20
    sites = []

    # Opening JSON file
    f = open('cast_list.json', )
    data = json.load(f)
    f.close()

    sites = data#[:1]
    index = list(range(0, len(sites)))

    print('start scrap cast ...')
    start = timeit.default_timer()

    # fetch series
    with ThreadPoolExecutor(max_workers=min(num_of_threads, len(sites))) as pool:
        pool.map(get_cast_direct, sites, index)

    time_scrap = timeit.default_timer()
    print('Time scrap: ', time_scrap - start)

    print(f'len of actors: {len(cast_list)}')


def actor_thumbnail():
    print('thumbnail actor start')

    # models.Movie.objects.all().delete()
    # return


    # actors = models.Actor.objects.all()
    actors = models.Movie.objects.all()
    print(len(actors))
    for actor in actors:
        print(actor)
        image = Image.open(actor.image)

        image.thumbnail((200, 160), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(actor.image.name)
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
            actor.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
            temp_thumb.close()

            actor.save()
        except:
            print(f'execption on {thumb_filename}')


def test():
    list = models.Movie.objects.filter(created_on__gt="2021-08-01")
    list2 = models.Series.objects.filter(created_on__gt="2021-08-01")

    for movie in list:
        d = movie.created_on
        jalili_date = jdatetime.date.fromgregorian(day=d.day,month=d.month,year=d.year)
        movie.created_on = str(jalili_date)
        movie.save()

    for serial in list2:
        d = serial.created_on
        jalili_date = jdatetime.date.fromgregorian(day=d.day,month=d.month,year=d.year)
        serial.created_on = str(jalili_date)
        serial.save()

