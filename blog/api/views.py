from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from .serializers import *
import logging
from filters import FilterBlog, FilterPost


_logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'owner__username']
    ordering_fields = ['title', 'updated_at']
    filterset_class = FilterBlog


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'author__username']
    ordering_fields = ['title', 'created_at', 'likes', 'views']
    filterset_class = FilterPost

    def retrieve(self, request, *args, **kwargs):
        _logger.debug('Rest request %s /posts/post.id received', request.method)
        post = self.get_object()
        if post:
            _logger.debug('Post exists increase view counter')
            post.update_views()
            serializer = self.get_serializer(post)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        _logger.debug('Rest request %s /posts/ received', request.method)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        _logger.debug('The received data is valid')
        blog = get_object_or_404(Blog, id=request.data['blog'])
        blog.update_updated_at()
        _logger.debug('New time of updated_at')
        if blog.authors.filter(id=request.user.id).exists() or request.user.id == blog.owner.id:
            _logger.debug('Request user passed the test. The post start saving')
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            _logger.warning('Request user did not passed the test. 400 response is returned')
            return Response('You are not author or owner of this blog', status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LikeViewSet(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pass

    def update(self, request, *args, **kwargs):
        _logger.debug('Rest request %s /like/ received', request.method)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        _logger.debug('Got post')
        if post.likes.filter(id=request.user.id).exists():
            _logger.debug('Delete like')
            post.likes.remove(request.user)
        else:
            _logger.debug('Add like')
            post.likes.add(request.user)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        serializer = PostSerializer(post)
        return Response(serializer.data)


class SubscriptionsViewSet(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pass

    def update(self, request, *args, **kwargs):
        _logger.debug('Rest request %s /subscriptions/ received', request.method)
        blog = get_object_or_404(Blog, id=self.kwargs['pk'])
        _logger.debug('Got blog')
        if blog.readers.filter(id=request.user.id).exists():
            _logger.debug('Delete subscription')
            blog.readers.remove(request.user)
        else:
            _logger.debug('Add subscription')
            blog.readers.add(request.user)
        user = get_object_or_404(User, id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class MyPosts(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user.id, is_published=True)
        return queryset


class MySubscriptions(mixins.ListModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Blog.objects.all()

    def list(self, request, *args, **kwargs):
        _logger.debug('Rest request %s /my_subscriptions/ received', request.method)
        queryset = Blog.objects.filter(readers=request.user.id)
        _logger.debug('Got all blogs in subscriptions request user')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BlogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)


class ChangePublish(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def update(self, request, *args, **kwargs):
        _logger.debug('Rest request %s /change_publish/ received', request.method)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        _logger.debug('Got post')
        if post.author == request.user:
            _logger.debug('Request user is post author')
            if post.is_published:
                _logger.debug('Remove from publications and delete time created_at')
                post.not_publish()
            else:
                _logger.debug('Add to publications and refresh time created_at')
                post.publish()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            _logger.warning('Request user did not author of this post. 400 response is returned')
            return Response('You are not author of this post', status=status.HTTP_400_BAD_REQUEST)
