from django.shortcuts import render
from .forms import ProductForm

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Product


def general(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render_to_response('rango/general.html', context_dict, context)


def list_view(request):
    context = RequestContext(request)
    context_dict = {}
    l = list(Product.objects.all())
    l.sort(key=lambda x: x.price, reverse=True)
    context_dict['products_all'] = l
    return render_to_response('rango/list-view.html', context_dict, context)


def grid_view(request):
    context = RequestContext(request)
    l = list(Product.objects.all())
    context_dict = {}
    l2 = []
    k1 = 0
    k2 = 1
    for x in l:
        try:
            l2[k1].append(x)
        except IndexError:
            l2.append([x])
        if k2 % 3 == 0:
            k1 += 1
        k2 += 1
    context_dict['products_all'] = l2
    return render_to_response('rango/grid-view.html', context_dict, context)


def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render_to_response('rango/index.html', context_dict, context)


def product_details(request, product_id):
    print('nice')
    context = RequestContext(request)
    product = Product.objects.get(id=product_id)
    context_dict = {'product': product}
    return render_to_response('rango/product_details.html', context_dict, context)


def about(request):
    string = "rango this is about page <br><a href='/rango'>Index</a>  "
    return HttpResponse(string)


def add_product(request):
    context = RequestContext(request)
    if request.method == 'POST':
        print('0')
        form = ProductForm(request.POST)
        print('1')
        if form.is_valid():
            print('2')
            form.save(commit=True)
            print('3')
            return render_to_response('rango/test.html', context, {'form': form})
        else:
            print('4')
            print(form.errors)
    else:
        form = ProductForm()
    return render_to_response('rango/test.html', {'form': form}, context)





