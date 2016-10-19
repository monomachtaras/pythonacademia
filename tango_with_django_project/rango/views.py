from django.shortcuts import render
from .forms import ProductForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Product, UserProfile


def general(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    # return render_to_response('rango/general.html', context_dict, context)
    return render(request, 'rango/general.html', context_dict, context)


def myaccount(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    # return render_to_response('rango/myaccount.html', context_dict, context)
    return render(request, 'rango/myaccount.html', context_dict, context)


def list_view(request):
    context = RequestContext(request)
    context_dict = {}
    l = list(Product.objects.all())
    l.sort(key=lambda x: x.price, reverse=True)
    context_dict['products_all'] = l
    # return render_to_response('rango/list-view.html', context_dict, context)
    return render(request, 'rango/list-view.html', context_dict, context)


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
    # return render_to_response('rango/grid-view.html', context_dict, context)
    return render(request, 'rango/grid-view.html', context_dict, context)


def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': 'I am a bald message'}
    # return render_to_response('rango/index.html', context_dict, context)
    return render(request, 'rango/index.html', context_dict, context)


def product_details(request, product_id):
    print('nice')
    context = RequestContext(request)
    product = Product.objects.get(id=product_id)
    context_dict = {'product': product}
    return render_to_response('rango/product_details.html', context_dict, context)


@login_required
def about(request):
    string = "rango this is about page <br><a href='/rango/user_logout'>Logout press hehe</a>  "
    return HttpResponse(string)

@login_required
def add_product(request):
    context = RequestContext(request)
    createdProduct = False
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # return render_to_response('rango/myaccount.html', context)
                print(user)
                print(user.is_authenticated)
                return HttpResponseRedirect('/rango/myaccount/')
                # return render(request, 'rango/register.html', context)
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