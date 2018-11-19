from django.db import models

# Create your models here.

class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # Meta类存储用于管理模型的额外信息，在这里设置一个特殊属性，让Django在需要
    # 时使用entries来表示多个条目
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return self.text[:50] + "..."