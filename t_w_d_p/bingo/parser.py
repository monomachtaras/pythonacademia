import re
import os
import datetime
import logging
import logging.handlers
import urllib.request
from django.db import transaction
from bs4 import BeautifulSoup
from .models import Number, Age, TimeDate, City, Images
import cv2
import numpy as np
from django.conf import settings as djangoSettings

logger_ = None


def get_logger():
    global logger_
    if logger_:
        return logger_
    else:
        logger_ = logging.getLogger(__name__)
        logger_.setLevel(logging.DEBUG)

        # create a file handler
        handler = logging.handlers.TimedRotatingFileHandler('logs/log.log', when='midnight')
        handler.setLevel(logging.INFO)
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)



        # add the handlers to the logger
        logger_.addHandler(handler)
        return logger_


def get_data_with_cities(htmlf):

    html = urllib.request.urlopen(htmlf).read()

    soup = BeautifulSoup(html, 'html.parser')
    l = soup.find_all('a', {'class': 'link'})

    pattern = re.compile('.*ukrgo\.com.*')
    result_list = [x for x in l if pattern.match(str(x))]
    for x in result_list:
        href = x['href']
        matchobj = re.match('.*http://(\D+)\.ukrgo.+', str(href))
        if matchobj:
            name = matchobj.group(1)
            try:
                City.objects.get(name=name)
            except:
                city = City()
                city.name = name
                city.html_href = href
                city.save()


def write_into_database():
    # init logger once
    get_logger()

    cities = City.objects.all()

    for city in cities:
        logger_.info(' city is running '+city.name)
        girls_of_city = get_girls_from_city(city.html_href)
        for girl in girls_of_city:  # set of html of girls
            list_with_info = get_info_from_girl(girl)
            logger_.info(' this girl is on fire '+str(list_with_info))
            if list_with_info:
                print(list_with_info)
                try:
                    number = get_number_object_from_number(list_with_info[0])
                    number.cities.add(get_city_object_from_city(list_with_info[1]))
                    number.ages.add(get_age_object_from_age(list_with_info[2]))
                    number.save()
                except Exception as e:
                    logger_.error('inside write into datebase'+e.__str__())

                # func mse takes much resources so use that func only with these conditions
                if len(list_with_info) > 4 \
                        and number.ages.all().count() < 2 \
                        and number.cities.all().count() < 2 \
                        and number.images.all().count() < 8:
                    number.images.add(get_image_object_from_image(list_with_info[4], city.name, list_with_info[3]))
                number.save()

                get_time_object_from_time(list_with_info[3], number)


def get_girls_from_city(htmlcity):

    html = urllib.request.urlopen(htmlcity).read()
    soup = BeautifulSoup(html, 'html.parser')
    lcity = soup.find_all('a', {'class': 'link_post'})

    l = []
    for x in lcity:
        l.append(x['href'])
    return set(l)


def get_info_from_girl(postofconcretegirl):
    try:
        html = urllib.urlopen(postofconcretegirl).read()
    except:
        try:
           logger_.info('got inside except UnicodeEncodeError ')
           matchobj = re.match('^(http.*?[0-9]{7,10}).*(\.html)$', str(postofconcretegirl))
           postofconcretegirl = matchobj.group(1) + matchobj.group(2)  # cut html here ascii doesnt read
           logger_.info(' postofconcrete girl ' + postofconcretegirl)
           html = urllib.request.urlopen(postofconcretegirl).read()
        except Exception as e:
           logger_.info(' error into unicodeerror '+e.__doc__)
           return None

    soup = BeautifulSoup(html, 'html.parser')

    listofinfo = getlistofinfo(soup, postofconcretegirl)

    if listofinfo:
        return listofinfo
    return None


def getlistofinfo(soup, postofconcretegirl):
    l = []

    # first find number
    getspansfromsoup = soup.find_all('span')
    number = ''  # type string
    for x in getspansfromsoup:
        matchobj = re.match('^<span>([0-9]+).*</span>$', str(x))
        if matchobj:
            number = int(matchobj.group(1))  # string type converted to int
            break
    if number:
        l.append(number)
    else:
        logger_.error(' number problem ' + str(getspansfromsoup))
        return None  # if number is incorrect

    #  here add city
    matchobj = re.match('^http://(\D+)\.ukrgo.+', str(postofconcretegirl))
    if matchobj:
        l.append(matchobj.group(1))
    else:
        logger_.error(' city problem ' + str(matchobj))
        return None

    #  here add age
    divs = soup.find_all('div')
    text = ''.join(str(divs[11].contents).split('\n'))
    matchobj = re.match('.*?</b>\s([0-9]{2}).*', text)
    if matchobj:
        age = matchobj.group(1)
        l.append(age)
    else:
        logger_.error(' age problem ' + text)
        return None

    #  here add time
    divcontent = divs[11].contents
    matchobj = re.match('.*?([0-9]{1,2}.[0-9]{1,2}.[0-9]{4}.[0-9]{1,2}.[0-9]{1,2}).*', str(divcontent))
    if matchobj:
        l.append(matchobj.group(1))
    else:
        logger_.error(' time problem ' + str(matchobj))
        now = datetime.datetime.now()
        l.append(str(now.day)+'.'+str(now.month)+'.'+str(now.year)+' '+str(now.hour)+':'+str(now.minute))

        # here add image
    image_img = soup.find_all('img', {'id': 'main_picture'})
    if image_img:
        l.append(image_img[0]['src'])

    return l


def get_age_object_from_age(ag):
    try:
        return Age.objects.get(age=ag)
    except Age.DoesNotExist:
        age = Age(age=ag)
        age.save()
        return age


def get_city_object_from_city(ci):
    return City.objects.get(name=ci)


def get_number_object_from_number(nu):
    try:
        return Number.objects.get(number=nu)
    except Number.DoesNotExist:
        number = Number(number=nu)
        number.save()
        return number


def get_image_object_from_image(info, city, time):
    cut_info = info[10:]
    static_path = djangoSettings.STATIC_ROOT +'/bingo/static'
    path = static_path + cut_info  # creating temp image
    file = open(path, 'wb')
    file.write(urllib.request.urlopen('http://' + str(city) + '.ukrgo.com' + info).read())
    file.close()

    images = list(Images.objects.all())
    if len(images) > 0:
        for image in images:
            original = cv2.imread(static_path + '/girls_images/' + str(image.name))
            new = cv2.imread(path)
            ms = mse(original, new)
            if ms < 300:
                logger_.info(' duplicate image, ms is =  ' + str(ms))
                os.remove(path)
                return image
    new_image = Images()
    name = str(Images.objects.latest('id').id+1) + cut_info[cut_info.find('.'):]
    new_image.name = name
    l = list_time(time)
    new_image.time = datetime.datetime(day=l[0], month=l[1], year=l[2], hour=l[3], minute=l[4])
    new_image.save()
    #  here move one file to other destination
    os.rename(path, static_path + '/girls_images/' + name)
    return new_image


def get_time_object_from_time(time, number):
    l = list_time(time)
    time_date = TimeDate()
    time_date.time = datetime.datetime(day=l[0], month=l[1], year=l[2], hour=l[3], minute=l[4])
    time_date.number = number
    time_date.save()
    return time_date


def list_time(time):
    l2 = re.findall('\d+', time)
    return [int(x) for x in l2]


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def test():
    original = cv2.imread("/home/ubuntu/PycharmProjects/pythonacademia/t_w_d_p/bingo/static/girls_images/73.jpg")
    contrast = cv2.imread("/home/ubuntu/PycharmProjects/pythonacademia/t_w_d_p/bingo/static/girls_images/211.jpg")
    print(mse(original, contrast))


@transaction.atomic
def first_method():
    get_logger()
    logger_.info(' first method ')
    number = Number()
    number.number = '0981988016'
    number.save()

    city = City.objects.get(name='ternopol')
    number.cities.add(city)
    age = Age()
    age.age = 25
    age.save()
    number.ages.add(age)
    time_date = TimeDate()
    time_date.time = datetime.datetime(day=9, month=2, year=2017, hour=20, minute=24)
    time_date.number = number
    time_date.save()

    file = open("/home/ubuntu/PycharmProjects/pythonacademia/t_w_d_p/bingo/static/girls_images/1.png", 'wb')
    file.write(urllib.request.urlopen('http://ternopol.ukrgo.com/pictures/ukrgo_id_15342569.png').read())
    file.close()
    newim = Images()
    newim.name = '1.png'
    newim.time = datetime.datetime(day=9, month=2, year=2017, hour=20, minute=24)
    newim.save()
    number.images.add(newim)
    number.save()
