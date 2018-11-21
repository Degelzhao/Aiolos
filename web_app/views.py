from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

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

def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据: 创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web_app:topics'))

    context = {'form': form}
    return render(request, 'web_app/new_topic.html', context)

def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        # 未提交数据: 创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('web_app:topic', args = [topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'web_app/new_entry.html', context)

def edit_entry(request, entry_id):
    """编辑已有条目"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('web_app:topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form }
    return render(request, 'web_app/edit_entry.html', context)
