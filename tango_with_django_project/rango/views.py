from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response


def general(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render_to_response('rango/general.html', context_dict, context)


def list_view(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render_to_response('rango/list-view.html', context_dict, context)


def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render_to_response('rango/index.html', context_dict, context)


def about(request):
    string = "rango this is about page <br><a href='/rango'>Index</a>  "
    return HttpResponse(string)






