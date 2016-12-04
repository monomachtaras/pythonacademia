from django.shortcuts import render
from .forms import ProductForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Product, Category, UserProfile
from django.views.generic import ListView, UpdateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

@login_required
def like(request):
    prod_id = request.GET['like_info']
    product = Product.objects.get(id=prod_id)
    product.like += 1
    product.save()
    return HttpResponse(product.like)

@login_required
def delete_product(request):
    prod_id = request.GET['delete_info']
    product = Product.objects.get(id=prod_id)
    product.delete()
    return HttpResponse('Product was deleted')


# @login_required
# def edit_product(request, edit_info):
#     context = RequestContext(request)
#     edited_product = False
#     if request.method == 'POST':
#         instance = Product.objects.get(id=edit_info)
#         form = ProductForm(request.POST, request.FILES, instance=instance)
#         if form.is_valid():
#             if 'product_logo' in request.FILES:
#                 form.product_logo = request.FILES['product_logo']
#             else:
#                 print('not in')
#             form.save()
#             edited_product = True
#             return render(request, 'rango/edit_product.html', {'edited_product': edited_product}, context)
#         else:
#             print(form.errors)
#     else:
#         product = Product.objects.get(id=edit_info)
#         d = product.__dict__
#         print(d)
#         d['category'] = product.category.id
#         d['product-logo'] = '../'+product.product_logo.url
#         pform = ProductForm(initial=d)
#         return render(request, 'rango/edit_product.html', {'form': pform, 'edited_product': edited_product,
#                                                            'product': product}, context)

class ProductUpdateView(UpdateView): # update product based on ClassBasedViews
    model = Product
    template_name = 'rango/edit_product.html'
    fields = [x for x in Product().__dict__.keys() if not x.startswith('_')] # exclude fields i dont need
    for x in range(len(fields)):
        if fields[x].__contains__('_'):
            fields[x] = fields[x][:fields[x].find('_')] # convert category_id to category
    success_url = '../index'


def general(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'boldmessage': 'I am a bald message', 'categories': categories}
    return render(request, 'rango/general.html', context_dict, context)


def my_account(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'categories': categories}
    return render(request, 'rango/my_account.html', context_dict, context)


# works good but i need paginator so I use FBView (later i will improve with CBW)
# class ProductListViev(ListView):
#     model = Product
#     template_name = 'rango/list_view.html'


def list_view(request, category_id='', page=None, search_info=''):
        context = RequestContext(request)
        context_dict = dict()
        if category_id: # if we specify category
            products_all = Product.objects.filter(category=category_id)
        elif search_info:
            print('search_info ',search_info)
            products_all = Product.objects.filter(name__icontains=search_info).order_by('price', 'name').reverse()
        else:
            products_all = Product.objects.all().order_by('price', 'name').reverse()
        if len(products_all) > 5:  # if len is < 5 not to display paginator
            paginator = Paginator(products_all, 5)
            context_dict['paginator'] = True
            try:
                products_all = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                products_all = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                products_all = paginator.page(paginator.num_pages)
        else:
            context_dict['paginator'] = False
        context_dict['object_list'] = products_all
        context_dict['category_id'] = category_id
        return render(request, 'rango/list_view.html', context_dict, context)


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
    return render(request, 'rango/grid_view.html', context_dict, context)


def index(request):
    context = RequestContext(request)
    categories = Category.objects.all()
    context_dict = {'boldmessage': 'I am a bald message', 'categories': categories}
    return render(request, 'rango/index.html', context_dict, context)


def product_details(request, product_id):
    context = RequestContext(request)
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)
    context_dict = {'product': product, 'categories': categories}
    return render(request, 'rango/product_details.html', context_dict, context)

@login_required
def about(request):
    string = "rango this is about page <br><a href='/rango/user_logout'>Logout press hehe</a>  "
    use = UserProfile()
    print(dir(use))
    return HttpResponse(string)

@login_required
def add_product(request):
    context = RequestContext(request)
    createdProduct = False
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            if 'product_logo' in request.FILES:
                form.product_logo = request.FILES['product_logo']
            else:
                print('not in')
            form.save()
            createdProduct = True
            return render(request, 'rango/add_product.html', {'createdProduct': createdProduct, 'categories': categories}, context)
        else:
            print(form.errors)
    else:
        form = ProductForm()
    return render(request, 'rango/add_product.html', {'form': form, 'createdProduct': createdProduct, 'categories': categories}, context)


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
    categories = Category.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'rango/my_account.html', {'categories': categories}, context)
            else:
                return render(request, 'rango/register.html', {'categories': categories}, context)
        else:
            print("Invalid login details: {}, {}".format(username, password))
            return render(request, 'rango/register.html', {'categories': categories})
    else:
        return render(request, 'rango/register.html', {'categories': categories}, context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/index')

