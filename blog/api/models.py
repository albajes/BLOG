import datetime

from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=400, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name='owner_blog', verbose_name='Создатель', on_delete=models.CASCADE)
    authors = models.ManyToManyField(User, related_name='author_blog', verbose_name='Авторы', blank=True)
    readers = models.ManyToManyField(User, related_name='readers', verbose_name='Читатели', blank=True)

    def update_updated_at(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        super(Blog, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Tags(models.Model):
    name = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    body = models.TextField(blank=False, null=False)
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tags, verbose_name='Теги', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_like', blank=True)
    views = models.IntegerField(default=0)
    blog = models.ForeignKey(Blog, verbose_name='Блог', on_delete=models.CASCADE)

    def update_views(self, *args, **kwargs):
        self.views = self.views + 1
        super(Post, self).save(*args, **kwargs)

    def publish(self, *args, **kwargs):
        self.is_published = True
        self.created_at = datetime.datetime.now()
        super(Post, self).save(*args, **kwargs)

    def not_publish(self, *args, **kwargs):
        self.is_published = False
        self.created_at = None
        super(Post, self).save(*args, **kwargs)

    @property
    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False, null=False, verbose_name='Текст')
    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']
