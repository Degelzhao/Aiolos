from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

urlpatterns = [
    # 登陆页面
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name = 'login'),
]