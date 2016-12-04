from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^like/$', views.like, name='like'),
    url(r'^index/', views.index, name='index'),
    url(r'^my_account/', views.my_account, name='my_account'),
    url(r'^register/', views.register, name='register'),
    url(r'^user_login/', views.user_login, name='user_login'),
    url(r'^user_logout/', views.user_logout, name='user_logout'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_product/', views.add_product, name='add_product'),
    url(r'^delete_product/', views.delete_product, name='delete_product'),
    url(r'^edit_product/(?P<pk>[0-9]+)$', views.ProductUpdateView.as_view(), name='edit_product'),
    url(r'^general/', views.general, name='general'),
    # url(r'^list_view/', views.ProductListViev.as_view(), name='list_view'), works fine but i need Paginator
    url(r'^list_view/(?P<category_id>[0-9]*)/(?P<page>[0-9]*)/(?P<search_info>.*)$', views.list_view, name='list_view'),
    url(r'^grid_view/', views.grid_view, name='grid_view'),
    url(r'^product_details/(?P<product_id>[0-9]+)$', views.product_details, name='product_details'),
]