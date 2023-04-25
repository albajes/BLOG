from django.test import TestCase

from .models import *


class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user_blog', password='1234')
        Blog.objects.create(title='blog_blog', description='blog_desc', owner=user)

    def test_title_label(self):
        blog = Blog.objects.get(description='blog_desc')
        field_label = blog._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_description_label(self):
        blog = Blog.objects.get(title='blog_blog')
        field_label = blog._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_name_max_length(self):
        blog = Blog.objects.get(title='blog_blog')
        max_length = blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 20)

    def test_description_max_length(self):
        blog = Blog.objects.get(description='blog_desc')
        max_length = blog._meta.get_field('description').max_length
        self.assertEqual(max_length, 400)

    def test_have_blog(self):
        blog = Blog.objects.get(title='blog_blog')
        all_blogs = Blog.objects.all()
        self.assertTrue(blog in all_blogs)


class TagsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tags.objects.create(name='Adventure')

    def test_name_max_length(self):
        tag = Tags.objects.get(name='Adventure')
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 10)

    def test_have_tag(self):
        tag = Tags.objects.get(name='Adventure')
        all_tags = Tags.objects.all()
        self.assertTrue(tag in all_tags)


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user_post', password='1234')
        blog = Blog.objects.create(title='blog_post', description='blog_post', owner=user)
        Post.objects.create(title='post_post', body='body_post', blog=blog, author=user)

    def test_title_label(self):
        post = Post.objects.get(body='body_post')
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_body_label(self):
        post = Post.objects.get(title='post_post')
        field_label = post._meta.get_field('body').verbose_name
        self.assertEquals(field_label, 'body')

    def test_name_max_length(self):
        post = Post.objects.get(title='post_post')
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_have_post(self):
        post = Post.objects.get(title='post_post')
        all_posts = Post.objects.all()
        self.assertTrue(post in all_posts)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='user_com', password='1234')
        blog = Blog.objects.create(title='blog_com', description='blog_com', owner=user)
        post = Post.objects.create(title='post_com', body='body_com', blog=blog, author=user)
        Comment.objects.create(body='com', author=user, post=post)

    def test_body_label(self):
        post = Post.objects.get(title='post_com')
        comment = Comment.objects.get(post=post)
        field_label = comment._meta.get_field('body').verbose_name
        self.assertEquals(field_label, 'Текст')

    def test_author_label(self):
        post = Post.objects.get(title='post_com')
        comment = Comment.objects.get(post=post)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'Автор')

    def test_post_label(self):
        user = User.objects.get(username='user_com')
        comment = Comment.objects.get(author=user)
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'Пост')

    def test_have_comment(self):
        comment = Comment.objects.get(body='com')
        all_comments = Comment.objects.all()
        self.assertTrue(comment in all_comments)
