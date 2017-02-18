import time
# import sys
import datetime
import re
import logging
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from .models import Number, Age, TimeDate, City, Images
from django.db.models import Count, Max
from django.views.generic import ListView, DetailView
from . import needtodelete
from .parser import write_into_database, first_method, get_data_with_cities

logger = logging.getLogger(__name__)

def new(request, page=None):
    #  if there are no cities
    # get_data_with_cities('http://ukrgo.com/view_subsection.php?id_subsection=146')
    # write_into_database()

    numbers = Number.objects.annotate(countcities=Count('cities', distinct=True), last_time=Max('timedate'),
                                      countages=Count('ages', distinct=True)).filter(countcities__lt=2,
                                                                      countages__lt=2).order_by('last_time').reverse()

    paginator = Paginator(numbers, 10)
    var = request.GET.get('page')
    if var:
        page = var
        logger.debug('method new: inside var')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        result_list = paginator.page(paginator.num_pages)

    context_dict = {'number_list': result_list, 'city_list': None, 'paginator': True}
    return render(request, 'list_view.html', context_dict)


class NumberListView(ListView):
    queryset = Number.objects.annotate(countcities=Count('cities'), countages=Count('ages'),
                                       last_time=Max('timedate')).filter(countcities__lt=2, countages__lt=2)\
        .order_by('last_time')
    template_name = 'list_view.html'
    context_object_name = 'number_list'


class DetailNumberView(DetailView):
    model = Number
    template_name = 'detail_view.html'
    context_object_name = 'number'