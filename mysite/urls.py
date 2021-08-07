"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib.auth import views
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import include, url, handler400, handler403, handler500
from django.urls import path
from mysite.sitemaps import StaticViewSitemap

sitemaps = {
    'sitemap': StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include("blog.urls")),
    path('', include('pages.urls')),
    path('users/', include('users.urls')), # new
    path('users/', include('django.contrib.auth.urls')), # new
    path('accounts/', include('allauth.urls')), 
    path('', include('enpApi.urls')),  
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


# Page Error Handling
handler400 = 'main.views.handle400'
handler403 = 'main.views.handle403'
handler404 = 'main.views.handle404'
handler500 = 'main.views.handle500'