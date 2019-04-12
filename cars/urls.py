from django.urls import path, re_path



from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('reset/', views.reset,name='reset_all'),
    re_path(r'^reset/(?P<countries>.+|^)/$', views.reset, name='reset'),
    path('overview/', views.overview, name='overview'),
    re_path(r'^reults/$',views.search, name='search'),
    re_path(r'^country/(?P<pk>\d+)/$',views.country, name='country'),
    re_path(r'^model/(?P<pk>\d+)/$',views.model, name='model'),
    re_path(r'^make/(?P<pk>\d+)/$',views.make, name='make'),
]
#|(\w+,)*\w+$|)