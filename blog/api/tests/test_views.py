from django.test import TestCase

from blog.api.views import *


class UserViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user_user', password='1234')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)


class BlogViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user_blog1', password='1234')
        User.objects.create_user(username='user_blog2', password='1234')
        Blog.objects.create(title='blog_blog', owner=user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blogs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_create_new_blog_with_not_login_user(self):
        response = self.client.post('/blogs/', {'title': 'new_blog'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_create_new_blog_with_login_user(self):
        self.client.login(username='user_blog1', password='1234')
        response = self.client.post('/blogs/', {'title': 'new_blog', 'description': 'new'})
        self.assertEqual(response.json()['owner_name'], 'user_blog1')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/blogs/')
        self.assertEqual(len(response.json()['results']), 2)
        self.assertEqual(response.status_code, 200)

    def test_update_exist_blog_by_no_owner(self):
        self.client.login(username='user_blog1', password='1234')
        response = self.client.post('/blogs/', {'title': 'new_blog1', 'description': 'new1'})
        self.assertEqual(response.status_code, 201)
        self.client.logout()
        self.client.login(username='user_blog2', password='1234')
        blog = Blog.objects.get(title='new_blog1')
        response = self.client.put('/blogs/' + str(blog.id) + '/', {'title': 'up_title', 'description': 'up_new'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'У вас недостаточно прав для выполнения данного действия.')
        response = self.client.delete('/blogs/' + str(blog.id) + '/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'У вас недостаточно прав для выполнения данного действия.')


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user_post1', password='1234')
        user2 = User.objects.create_user(username='user_post2', password='1234')
        blog1 = Blog.objects.create(title='blog_post1', owner=user)
        blog2 = Blog.objects.create(title='blog_post2', owner=user2)
        Post.objects.create(title='post_post1', author=user, blog=blog1)
        Post.objects.create(title='post_post2', author=user2, blog=blog2)
        Post.objects.create(title='post_post3', author=user, blog=blog1, is_published=True)
        Post.objects.create(title='post_post4', author=user2, blog=blog2, is_published=True)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)
        blog1 = Blog.objects.get(title='blog_post1')
        response = self.client.get('/posts/?blog=' + str(blog1.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        blog2 = Blog.objects.get(title='blog_post2')
        response = self.client.get('/posts/?blog=' + str(blog2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

    def test_create_new_post_with_not_login_user(self):
        response = self.client.post('/posts/', {'title': 'new_post_title'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_create_new_post_with_login_user(self):
        self.client.login(username='user_post1', password='1234')
        blog1 = Blog.objects.get(title='blog_post1')
        response = self.client.post('/posts/', {'title': 'new_post', 'body': 'new', 'blog': blog1.id,
                                                'is_published': True})
        self.assertEqual(response.json()['author']['username'], 'user_post1')
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/posts/')
        self.assertEqual(len(response.json()['results']), 3)
        self.assertEqual(response.status_code, 200)

    def test_create_new_post_not_blog_author_or_owner(self):
        self.client.login(username='user_post2', password='1234')
        blog1 = Blog.objects.get(title='blog_post1')
        response = self.client.post('/posts/', {'title': 'new_post', 'body': 'new', 'blog': blog1.id,
                                                'is_published': True})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'You are not author or owner of this blog')

    def test_create_new_post_blog_author_not_owner(self):
        self.client.login(username='user_post1', password='1234')
        user2 = User.objects.get(username='user_post2')
        blog1 = Blog.objects.get(title='blog_post1')
        response = self.client.put('/blogs/' + str(blog1.id) + '/', {'title': 'blog_post1', 'description': 'new1',
                                                                'authors': [user2.id]}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username='user_post2', password='1234')
        response = self.client.post('/posts/', {'title': 'new_post', 'body': 'new', 'blog': blog1.id,
                                                 'is_published': True})
        self.assertEqual(response.status_code, 201)

    def test_change_views_post(self):
        self.client.login(username='user_post1', password='1234')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)
        self.assertEqual(response.json()['results'][0]['views'], 0)
        self.assertEqual(response.json()['results'][1]['views'], 0)
        post1_id = response.json()['results'][0]['id']
        post2_id = response.json()['results'][1]['id']
        response = self.client.get('/posts/' + str(post1_id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['views'], 1)
        response = self.client.get('/posts/' + str(post2_id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['views'], 1)


class CommentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='user_comment1', password='1234')
        user2 = User.objects.create_user(username='user_comment2', password='1234')
        blog1 = Blog.objects.create(title='blog_comment1', owner=user)
        blog2 = Blog.objects.create(title='blog_comment2', owner=user2)
        post1 = Post.objects.create(title='post_comment1', author=user, blog=blog1, is_published=True)
        post2 = Post.objects.create(title='post_comment2', author=user2, blog=blog2, is_published=True)
        Comment.objects.create(body='com1', author=user, post=post1)
        Comment.objects.create(body='com2', author=user2, post=post2)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)

    def test_create_new_comment_with_not_login_user(self):
        response = self.client.post('/comments/', {'body': 'comment_title', 'post': 1})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_create_new_comment_with_login_user(self):
        self.client.login(username='user_comment1', password='1234')
        post1 = Post.objects.get(title='post_comment1')
        post2 = Post.objects.get(title='post_comment2')
        response = self.client.post('/comments/', {'body': 'new_comment1', 'post': post1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['author']['username'], 'user_comment1')
        response = self.client.post('/comments/', {'body': 'new_comment2', 'post': post2.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['author']['username'], 'user_comment1')
        response = self.client.get('/comments/')
        self.assertEqual(len(response.json()['results']), 4)
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        self.client.login(username='user_comment2', password='1234')
        response = self.client.post('/comments/', {'body': 'new_comment3', 'post': post1.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['author']['username'], 'user_comment2')
        response = self.client.post('/comments/', {'body': 'new_comment4', 'post': post2.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['author']['username'], 'user_comment2')
        response = self.client.get('/comments/')
        self.assertEqual(len(response.json()['results']), 6)
        self.assertEqual(response.status_code, 200)


class TagsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='user_tags', password='1234')
        Tags.objects.create(name='Advanture')
        Tags.objects.create(name='Films')
        Tags.objects.create(name='Music')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 3)

    def test_create_new_tag_with_not_login_user(self):
        response = self.client.post('/tags/', {'name': 'new_tag'})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_create_new_tag_with_login_user(self):
        self.client.login(username='user_tags', password='1234')
        response = self.client.post('/tags/', {'name': 'new_tag'})
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/tags/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 4)


class LikeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user_like', password='1234')
        blog1 = Blog.objects.create(title='blog_like', owner=user1)
        Post.objects.create(title='post_like', author=user1, blog=blog1, is_published=True)

    def test_add_like_to_post_with_not_login_user(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['title'], 'post_like')
        self.assertEqual(response.json()['results'][0]['likes'], [])
        self.assertEqual(response.json()['results'][0]['like_count'], 0)
        post1 = Post.objects.get(title='post_like')
        response = self.client.patch('/like/' + str(post1.id) + '/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_add_and_remove_like_to_post_with_login_user(self):
        self.client.login(username='user_like', password='1234')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['title'], 'post_like')
        self.assertEqual(response.json()['results'][0]['likes'], [])
        self.assertEqual(response.json()['results'][0]['like_count'], 0)
        post1 = Post.objects.get(title='post_like')
        user1 = User.objects.get(username='user_like')
        response = self.client.patch('/like/' + str(post1.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], [user1.id])
        self.assertEqual(response.json()['like_count'], 1)
        response = self.client.patch('/like/' + str(post1.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], [])
        self.assertEqual(response.json()['like_count'], 0)


class SubscriptionsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user_sub1', password='1234')
        User.objects.create_user(username='user_sub2', password='1234')
        Blog.objects.create(title='blog_sub', owner=user1)

    def test_get_subscription_with_not_login_user(self):
        blog1 = Blog.objects.get(title='blog_sub')
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_add_and_remove_subscription_with_login_user(self):
        blog1 = Blog.objects.get(title='blog_sub')
        user1 = User.objects.get(username='user_sub1')
        user2 = User.objects.get(username='user_sub2')
        self.assertEqual(list(blog1.readers.all()), [])
        self.client.login(username='user_sub2', password='1234')
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(blog1.readers.all())), 1)
        self.assertEqual(list(blog1.readers.all()), [user2])
        self.client.logout()
        self.client.login(username='user_sub1', password='1234')
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(blog1.readers.all())), 2)
        self.assertEqual(list(blog1.readers.all()), [user2, user1])
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(blog1.readers.all())), 1)
        self.assertEqual(list(blog1.readers.all()), [user2])


class MyPostsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user_mp1', password='1234')
        user2 = User.objects.create_user(username='user_mp2', password='1234')
        user3 = User.objects.create_user(username='user_mp3', password='1234')
        blog1 = Blog.objects.create(title='blog1', owner=user1)
        blog2 = Blog.objects.create(title='blog2', owner=user2)
        Post.objects.create(title='post1', author=user1, blog=blog1, is_published=True)
        Post.objects.create(title='post2', author=user1, blog=blog1, is_published=True)
        Post.objects.create(title='post3', author=user2, blog=blog2, is_published=True)
        Post.objects.create(title='post4', author=user2, blog=blog2, is_published=True)
        Post.objects.create(title='post5', author=user2, blog=blog2, is_published=True)

    def test_get_my_posts_with_not_login_user(self):
        response = self.client.get('/my_posts/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_get_my_posts_with_login_user(self):
        self.client.login(username='user_mp1', password='1234')
        response = self.client.get('/my_posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 2)
        self.client.logout()
        self.client.login(username='user_mp2', password='1234')
        response = self.client.get('/my_posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 3)
        self.client.logout()
        self.client.login(username='user_mp3', password='1234')
        response = self.client.get('/my_posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)


class MySubscriptionsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user_sub1', password='1234')
        user2 = User.objects.create_user(username='user_sub2', password='1234')
        User.objects.create_user(username='user_sub3', password='1234')
        Blog.objects.create(title='blog_sub1', owner=user1)
        Blog.objects.create(title='blog_sub2', owner=user1)
        Blog.objects.create(title='blog_sub3', owner=user2)
        Blog.objects.create(title='blog_sub4', owner=user2)
        Blog.objects.create(title='blog_sub5', owner=user2)

    def test_get_my_subscriptions_with_not_login_user(self):
        response = self.client.get('/my_subscriptions/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_get_my_subscriptions_with_login_user(self):
        self.client.login(username='user_sub1', password='1234')
        user1 = User.objects.get(username='user_sub1')
        blog1 = Blog.objects.get(title='blog_sub3')
        response = self.client.get('/my_subscriptions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/my_subscriptions/')
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['title'], 'blog_sub3')
        self.assertEqual(response.json()['results'][0]['readers'], [user1.id])
        self.client.logout()
        self.client.login(username='user_sub2', password='1234')
        user2 = User.objects.get(username='user_sub2')
        response = self.client.get('/my_subscriptions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/my_subscriptions/')
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json()['results'][0]['title'], 'blog_sub3')
        self.assertEqual(response.json()['results'][0]['readers'], [user1.id, user2.id])
        response = self.client.put('/subscriptions/' + str(blog1.id) + '/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/my_subscriptions/')
        self.assertEqual(response.json()['count'], 0)


class ChangePublish(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(username='user_chan1', password='1234')
        user2 = User.objects.create_user(username='user_chan2', password='1234')
        blog1 = Blog.objects.create(title='blog_chan1', owner=user1)
        blog2 = Blog.objects.create(title='blog_chan2', owner=user2)
        Post.objects.create(title='post_chan1', author=user1, blog=blog1)
        Post.objects.create(title='post_chan2', author=user2, blog=blog2)

    def test_changePublish_with_not_login_user(self):
        post = Post.objects.get(title='post_chan1')
        response = self.client.put('/change_publish/' + str(post.id) + '/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()['detail'], 'Учетные данные не были предоставлены.')

    def test_changePublish_if_user_not_author(self):
        self.client.login(username='user_chan1', password='1234')
        post = Post.objects.get(title='post_chan2')
        response = self.client.put('/change_publish/' + str(post.id) + '/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'You are not author of this post')

    def test_changePublish_if_user_author(self):
        self.client.login(username='user_chan2', password='1234')
        post = Post.objects.get(title='post_chan2')
        self.assertEqual(post.is_published, False)
        response = self.client.put('/change_publish/' + str(post.id) + '/')
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(title='post_chan2')
        self.assertEqual(post.is_published, True)
        response = self.client.put('/change_publish/' + str(post.id) + '/')
        self.assertEqual(response.status_code, 200)
        post = Post.objects.get(title='post_chan2')
        self.assertEqual(post.is_published, False)