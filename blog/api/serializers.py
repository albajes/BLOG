from datetime import datetime

from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Post, Blog, Comment, Tags


class BlogSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description', 'owner', 'owner_name', 'authors', 'updated_at', 'readers']


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.SerializerMethodField('get_blogs')

    class Meta:
        model = User
        fields = ['id', 'username', 'subscriptions']

    @staticmethod
    def get_blogs(obj):
        user_id = obj.id
        blogs = Blog.objects.filter(readers__id=user_id).values('id', 'title')
        return blogs


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all(), write_only=True)
    blog_data = BlogSerializer(source='blog', read_only=True)
    like_count = serializers.ReadOnlyField(source='number_of_likes')

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author', 'blog_data', 'is_published', 'likes', 'like_count', 'views', 'blog',
                  'tags', 'created_at']
        extra_kwargs = {
            'views': {'read_only': True}, 'source': 'post.views'
        }


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    # author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        exclude = ['created_at']
        extra_kwargs = {
            'post': {'write_only': True},
            'post_title': {'read_only': True, 'source': 'post.title'},
            'author_name': {'read_only': True}
        }


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'
