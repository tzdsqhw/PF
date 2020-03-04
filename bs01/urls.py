"""bs01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from bysjapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^index/$',views.index,name='index'),
    url(r'shop/(?P<goodtype>\w+)/$',views.shop,name='shop'),
    url(r'^pet/(?P<speci>\w+)/$',views.pet,name="pets"),
    url(r'^person/(?P<type>\w+)/$',views.personp,name="person"),
    url(r'^singleuser/(?P<username>\w+)/$',views.singlep,name="singleuser"),
    url(r'^singlegood/(?P<gid>\w+)/$',views.singleg,name="singlegood"),
    url(r'^singlepet/(?P<pid>\w+)/$',views.singlepet,name="singlepet"),
    url(r'^about/$', views.about, name="about"),
    url(r'^login/$', views.logIn, name="login"),
    url(r'^register/$', views.register, name="register"),
    url(r'^check_code$',views.check_code,name='check_code'),
    url(r'^logout/$', views.logOut, name="logout"),
    url(r'^sp_logout/$', views.sp_logOut, name="sp_logout"),
    url(r'demp/$',views.demp,name="demp"),
    url(r'^like/$',views.like, name='like'),
    url(r'^addgood/$',views.addg, name='addgood'),
    url(r'^delgood/$',views.deletg, name='delgood'),
    url(r'^deld/$',views.deletd, name='deld'),
    url(r'^shopcar/$',views.shopcar,name="shopcar"),
    url(r'^oder/$',views.oder,name='oder'),
    url(r'^information/$',views.informationcheck,name='infor'),
    url(r'^admin/upload/$',views.upload_lg,name='upload_lg'),
    url(r'^admin/upload_sel/$', views.upload_sel, name='upload_sel'),
    url(r'^admin/upload/(?P<whc>\w+)_(?P<optype>\w+)/$',views.upload,name="upload"),
    url(r'^admin/ode_up/(?P<oid>\w+)$',views.oder_up,name="ode_up"),


]
