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
    context = {'topics':topics}
    return render(request, 'web_app/topics.html', context)

def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    # 获取topic_id的值
    topic = Topic.objects.get(id = topic_id)
    # 获取与该主题相关联的条目，按时间降序排列
    entries = topic.entry_set.order_by('-date_added')
    # 将主题和条目存储在字典context中
    context = {'topic':topic, 'entries':entries}
    return render(request, 'web_app/topic.html', context)