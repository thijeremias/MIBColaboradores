"""mibcolaboradores URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from mibcolaboradores import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.do_login, name = 'login'),
    url(r'^cadastrar$', views.cadastrar, name = 'cadastrar'),
    url(r'^home$',views.home, name = 'home'),
    url(r'^logout$',views.do_logout, name = 'logout'),
    url(r'^consultar$',views.consultar, name = 'consultar'),
    url(r'^editar/(?P<pk>[0-9]+)/$',views.editar, name = 'editar'),#Url que recebe a chave primaria como argumento para abrir a página
    url(r'^transferir$',views.transferir, name = 'transferir'),
    url(r'^administrativo$',views.administrativo, name = 'administrativo'),
    url(r'^\w+$',views.erro, name = 'erro'),
]
