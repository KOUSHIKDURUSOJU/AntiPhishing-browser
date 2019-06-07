# dprojx/urls.py
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from dappx import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^special/',views.special,name='special'),
    url(r'^dappx/',include('dappx.urls')),
    path('dappx/', include('django.contrib.auth.urls')),
    url(r'^logout/$', views.user_logout, name='logout'),
]