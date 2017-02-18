from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^new/(?P<page>[0-9]*)$', views.new, name='new'),
    url(r'^list_view/', views.NumberListView.as_view(), name='list_view'),
    url(r'^details_url/(?P<pk>[0-9]*)', views.DetailNumberView.as_view(), name='detail_view'),

]