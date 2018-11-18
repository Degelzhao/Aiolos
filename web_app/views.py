from django.shortcuts import render
from .models import Topic

# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'web_app/index.html')

def topics(request):  # request: Django从服务器收到的request对象
    """显示所有主题"""
    # 查询数据库 -- 请求提供Topic对象，并按属性date_added对他们进行排序
    topics = Topic.objects.order_by('date_added')
    # 定义一个将要发送给模板的上下文
    context = {'topic':topics}
    return render(request, 'web_app/topics.html', context)