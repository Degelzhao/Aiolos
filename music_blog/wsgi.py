"""
WSGI config for music_blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling    #导入了帮助正确提供静态文件的Cling,并使用它来启动应用程序


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_blog.settings')

application = Cling(get_wsgi_application())
