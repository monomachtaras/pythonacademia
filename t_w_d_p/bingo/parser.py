import re
import os
import datetime
import logging
import logging.handlers
import urllib
import unicodedata
from bs4 import BeautifulSoup
from .models import Number, Age, TimeDate, City, Images
import cv2
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
from django.conf import settings as djangoSettings

logger = None


def get_logger():
    global logger
    if logger:
        return logger
    else:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # create a file handler
        handler = logging.handlers.TimedRotatingFileHandler('log1.log', when='midnight')
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(handler)
        return logger


def get_data_with_cities(htmlf):

    html = urllib.urlopen(htmlf).read()

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

    #cities = City.objects.all()
    cities = City.objects.get(id=1)


    for city in cities:
        logger.info(' city is running '+city.name)
        girls_of_city = get_girls_from_city(city.html_href)
        for girl in girls_of_city:  # set of html of girls
            list_with_info = get_info_from_girl(girl)
            logger.info(' this girl is on fire '+str(list_with_info))
            if list_with_info:
                number = get_number_object_from_number(list_with_info[0])
                number.cities.add(get_city_object_from_city(list_with_info[1]))
                number.ages.add(get_age_object_from_age(list_with_info[2]))

                # func mse takes much resources so use that func only with these conditions
                if len(list_with_info) > 4 \
                        and number.ages.all().count() < 2 \
                        and number.cities.all().count() < 2 \
                        and number.images.all().count() < 8:
                    number.images.add(get_image_object_from_image(list_with_info[4], city.name))
                number.save()

                get_time_object_from_time(list_with_info[3], number)


def get_girls_from_city(htmlcity):

    html = urllib.urlopen(htmlcity).read()
    soup = BeautifulSoup(html, 'html.parser')
    lcity = soup.find_all('a', {'class': 'link_post'})

    l = []
    for x in lcity:
        l.append(x['href'])
    return set(l)


def get_info_from_girl(postofconcretegirl):

    try:
        html = urllib.urlopen(postofconcretegirl).read()
    except UnicodeEncodeError:
        logger.info('got inside except UnicodeEncodeError ')
        matchobj = re.match('^(http.*?[0-9]{7,10}).*(\.html)$', str(postofconcretegirl))
        postofconcretegirl = matchobj.group(1) + matchobj.group(2)  # cut html here ascii doesnt read
        logger.info(' postofconcrete girl ' + postofconcretegirl)
        html = urllib.request.urlopen(postofconcretegirl).read()
        logger.info(' error into unicodeerror ')
    except Exception as e:
        logger.info(' error into get_infoFrom_girl ' + e.__doc__)
        return

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
        logger.error(' number problem ' + str(matchobj))
        return None  # if number is incorrect

    #  here add city
    matchobj = re.match('^http://(\D+)\.ukrgo.+', str(postofconcretegirl))
    if matchobj:
        l.append(matchobj.group(1))
    else:
        logger.error(' city problem ' + str(matchobj))
        return None

    #  here add age
    divs = soup.find_all('div')
    text = str(divs[11].contents)
    matchobj = re.match('.*?</b>\s([0-9]{2}).*', text)
    if matchobj:
        age = matchobj.group(1)
        l.append(age)
    else:
        logger.error(' age problem ' + text)
        return None

    #  here add time
    divcontent = divs[11].contents
    matchobj = re.match('.*?([0-9]{1,2}.[0-9]{1,2}.[0-9]{4}.[0-9]{1,2}.[0-9]{1,2}).*', str(divcontent))
    if matchobj:
        l.append(matchobj.group(1))
    else:
        logger.error(' time problem ' + str(matchobj))
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


def get_image_object_from_image(info, city):
    cut_info = info[10:]
    static_path = djangoSettings.STATIC_ROOT +'/bingo/static'
    path = static_path + cut_info  # creating temp image
    file = open(path, 'wb')
    file.write(urllib.urlopen('http://' + str(city) + '.ukrgo.com' + info).read())
    file.close()

    images = list(Images.objects.all())
    if len(images) > 0:
        for image in images:
            original = cv2.imread(static_path + '/girls_images/' + str(image.name))
            new = cv2.imread(path)
            ms = mse(original, new)
            if ms < 300:
                logger.info(' duplicate image, ms is =  ' + str(ms))
                os.remove(path)
                return image
    new_image = Images()
    try:
        name = str(Images.objects.latest('id').id+1) + cut_info[cut_info.find('.'):]
    except:
        name = str(1) + cut_info[cut_info.find('.'):]
    new_image.name = name
    new_image.save()
    #  here move one file to other destination
    os.rename(path, static_path + '/girls_images/' + name)
    return new_image


def get_time_object_from_time(time, number):
    l2 = re.findall('\d+', time)
    l = [int(x) for x in l2]

    time_date = TimeDate()
    time_date.time = datetime.datetime(day=l[0], month=l[1], year=l[2], hour=l[3], minute=l[4])
    time_date.number = number
    time_date.save()




def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB, title):
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = ssim(imageA, imageB)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap=plt.cm.gray)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap=plt.cm.gray)
    plt.axis("off")

    # show the images
    plt.show()


def imageses():
    original = cv2.imread("/home/ubuntu/images/chooko.jpeg")
    contrast = cv2.imread("/home/ubuntu/images/tea-006.jpg")
    shopped = cv2.imread("/home/ubuntu/images/lviv.jpeg")

    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    shopped = cv2.cvtColor(shopped, cv2.COLOR_BGR2GRAY)

    fig = plt.figure("Images")
    images = ("Original", original), ("Contrast", contrast), ("Photoshopped", shopped)

    # loop over the images
    for (i, (name, image)) in enumerate(images):
        # show the image
        ax = fig.add_subplot(1, 3, i + 1)
        ax.set_title(name)
        plt.imshow(image, cmap=plt.cm.gray)
        plt.axis("off")

    # show the figure
    plt.show()

    # compare the images
    compare_images(original, original, "Original vs. Original")
    compare_images(original, contrast, "Original vs. Contrast")
    compare_images(original, shopped, "Original vs. Photoshopped")


def test():
    original = cv2.imread("/home/ubuntu/PycharmProjects/pythonacademia/t_w_d_p/bingo/static/girls_images/73.jpg")
    contrast = cv2.imread("/home/ubuntu/PycharmProjects/pythonacademia/t_w_d_p/bingo/static/girls_images/211.jpg")
    print(mse(original, contrast))