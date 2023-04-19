from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters, ModelChoiceFilter

from .permisisions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from .serializers import *


class FilterBlog(filters.FilterSet):
    updated_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Blog
        fields = ['updated_at']


class FilterPost(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()
    tags = ModelChoiceFilter(queryset=Tags.objects.all())
    blog = ModelChoiceFilter(queryset=Blog.objects.all())

    class Meta:
        model = Post
        fields = ['created_at', 'tags', 'blog']


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
        post = self.get_object()
        if post:
            post.update_views()
            serializer = self.get_serializer(post)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        blog = get_object_or_404(Blog, id=request.data['blog'])
        blog.update_updated_at()
        if blog.authors.filter(id=request.user.id).exists() or request.user.id == blog.owner.id:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
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
    def get_queryset(self):
        pass

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        serializer = PostSerializer(post)
        return Response(serializer.data)


class SubscriptionsViewSet(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pass

    def update(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, id=self.kwargs['pk'])
        if blog.readers.filter(id=request.user.id).exists():
            blog.readers.remove(request.user)
        else:
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
        queryset = Blog.objects.filter(readers=request.user.id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BlogSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)


class ChangePublish(mixins.UpdateModelMixin, GenericViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def update(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.author == request.user:
            if post.is_published:
                post.not_publish()
            else:
                post.publish()
            serializer = PostSerializer(post)
            return Response(serializer.data)
        else:
            return Response('You are not author of this post', status=status.HTTP_400_BAD_REQUEST)

