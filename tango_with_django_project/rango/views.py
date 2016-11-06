from django.shortcuts import render
from .forms import ProductForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Product, UserProfile
import json
from django.core import serializers

@login_required
def like(request):
    prod_id = request.GET['like_info']
    product = Product.objects.get(id=prod_id)
    product.like += 1
    product.save()
    return HttpResponse(product.like)

def test(request):
    context = RequestContext(request)
    return render(request, 'rango/test.html', {}, context)


def general(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render(request, 'rango/general.html', context_dict, context)


def myaccount(request):
    context = RequestContext(request)
    context_dict = dict()
    return render(request, 'rango/myaccount.html', context_dict, context)


def show_category(request, category_name):
    context = RequestContext(request)
    context_dict = dict()
    context_dict['products_all'] = Product.objects.filter(category=category_name)
    return render(request, 'rango/list-view.html', context_dict, context)


def search(request):
    context = RequestContext(request)
    search_info = request.POST['search_info']
    listfilter= Product.objects.filter(name__icontains=search_info).order_by('price', 'name').reverse()
    return render(request, 'rango/search.html', {'products_filter': listfilter}, context)


def list_view(request):
        context = RequestContext(request)
        context_dict = dict()
        context_dict['products_all'] = Product.objects.all().order_by('price', 'name').reverse()
        return render(request, 'rango/list-view.html', context_dict, context)

# def list_view(request):
#     context = RequestContext(request)
#     context_dict = dict()
#     context_dict['products_all'] = Product.objects.all().order_by('price', 'name').reverse()
#     return render(request, 'rango/list-view.html', context_dict, context)


def grid_view(request):
    context = RequestContext(request)
    l = Product.objects.all().order_by('price')
    context_dict = dict()
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
    context_dict['products_all'] = l2 # l2 is list of lists  [ [], [], [] ]
    # return render_to_response('rango/grid-view.html', context_dict, context)
    return render(request, 'rango/grid-view.html', context_dict, context)


def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    return render(request, 'rango/index.html', context_dict, context)


def product_details(request, product_id):
    context = RequestContext(request)
    product = Product.objects.get(id=product_id)
    context_dict = {'product': product}
    return render(request, 'rango/product_details.html', context_dict, context)

@login_required
def about(request):
    string = "rango this is about page <br><a href='/rango/user_logout'>Logout press hehe</a>  "
    use = UserProfile()
    print(dir(use))
    return HttpResponse(string)


def add_product(request):
    context = RequestContext(request)
    createdProduct = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if 'product_logo' in request.FILES:
                print('is is')
                form.product_logo = request.FILES['product_logo']
                print(form)
            else:
                print('not in')
            form.save()
            createdProduct = True
            return render_to_response('rango/add_product.html', {'form': form, 'createdProduct': createdProduct},
                                      context)
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'rango/add_product.html', {'form': form, 'createdProduct': createdProduct}, context)


def register(request):
    context = RequestContext(request)
    createdUser = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'user_logo' in request.FILES:
                print('ababagalamaga')
                profile.user_logo = request.FILES['user_logo']
                profile.save()
                createdUser = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form,
                                                   'createdUser': createdUser}, context)


def user_login(request):
    context = RequestContext(request)
    context_dict = dict()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'rango/myaccount.html', context_dict, context)
            else:
                return render(request, 'rango/register.html', context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, 'rango/register.html', {})
    else:
        return render(request, 'rango/register.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/index')

