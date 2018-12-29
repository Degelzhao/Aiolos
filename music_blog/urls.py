"""music_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
#from django.contrib import admin
#from django.urls import path
from django.conf.urls import include,url
from django.contrib import admin

#urlpatterns = [
#    path('admin/', admin.site.urls),
#]

urlpatterns = [
    url(r'^admin/',include(admin.site.urls)),
    # 包含users的url,实参namespace能够将users的URL同项目中的其他URL区分开
    url(r'^users/',include('users.urls',namespace='users')),
    # 包含web_app的url,实参namespace能够将web_app的URL同项目中的其他URL区分开
    url(r'', include('web_app.urls',namespace = 'web_app')),
]