from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/$', views.new, name='new'),
    url(r'^list_view/', views.NumberListView.as_view(), name='list_view'),

]