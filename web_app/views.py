from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'web_app/index.html')

@login_required
def topics(request):  # request: Django从服务器收到的request对象
    """显示所有主题"""
    # 查询数据库 -- 请求提供Topic对象，并按属性date_added对他们进行排序
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 定义一个将要发送给模板的上下文
    context = {'topics':topics}
    return render(request, 'web_app/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    # 获取topic_id的值
    topic = get_object_or_404(Topic, id=topic_id)
    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    # 获取与该主题相关联的条目，按时间降序排列
    entries = topic.entry_set.order_by('-date_added')
    # 将主题和条目存储在字典context中
    context = {'topic':topic, 'entries':entries}
    return render(request, 'web_app/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据: 创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('web_app:topics'))

    context = {'form': form}
    return render(request, 'web_app/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404
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

@login_required
def edit_entry(request, entry_id):
    """编辑已有条目"""
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

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
