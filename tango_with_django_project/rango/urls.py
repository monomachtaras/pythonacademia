from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),
    url(r'^about/', views.about, name='about'),
    url(r'^general/', views.general, name='general'),
    url(r'^list_view/', views.list_view, name='list_view'),
]