from django.shortcuts import render
from django.template import RequestContext
from .models import Number, Age, TimeDate, City, Images
from django.db.models import Count
import parser
from django.views.generic import ListView
import time
# import sys
# sys.path.append("../t_w_d_p/bingo")
# import logger
import datetime


def new(request):
    #  if there are no cities
    # parser.get_data_with_cities('http://ukrgo.com/view_subsection.php?id_subsection=146')
    # starttime = time.time()
    # parser.write_into_database()
    # endtime = time.time()
    # print(endtime-starttime)

    now = datetime.datetime.now()
    print(now)






    context_dict = {'boldmessage': 'I am a bald message'}
    return render(request, 'about_us.html', context_dict)


class NumberListView(ListView):
    queryset = Number.objects.annotate(countcities=Count('cities'), countages=Count('ages')).filter(countcities__lt=2,
                                                                                                    countages__lt=2,
                                                                                                    )
    template_name = 'list_view.html'
    context_object_name = 'number_list'


def write_into_database(lis):
    number = Number.objects.get(number=int(lis[0]))

    if number:
        pass
    else:
        number = Number()
        number.number = int(lis[0])
        number.save()

    city = City.objects.get(name=lis[1])
    if city:
        pass
    else:
        city = City()
        city.name = lis[1]
