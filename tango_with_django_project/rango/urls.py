from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^like/$', views.like, name='like'),
    url(r'^test/', views.test, name='test'),
    url(r'^index/', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^my_account/', views.my_account, name='my_account'),
    url(r'^register/', views.register, name='register'),
    url(r'^user_login/', views.user_login, name='user_login'),
    url(r'^user_logout/', views.user_logout, name='user_logout'),
    url(r'^about/', views.about, name='about'),
    url(r'^add_product/', views.add_product, name='add_product'),
    url(r'^delete_product/', views.delete_product, name='delete_product'),
    url(r'^edit_product/(?P<edit_info>[0-9]+)$', views.edit_product, name='edit_product'),
    url(r"^category/(?P<category_name>[A-Za-z&' ]+)$", views.show_category, name='show_category'),
    url(r'^general/', views.general, name='general'),
    url(r'^list_view/', views.list_view, name='list_view'),
    url(r'^grid_view/', views.grid_view, name='grid_view'),
    url(r'^product_details/(?P<product_id>[0-9]+)$', views.product_details, name='product_details'),
]