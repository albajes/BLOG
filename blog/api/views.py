from rest_framework import permissions, viewsets, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .permisisions import IsOwnerOrReadOnly, IsAuthorOrReadOnly
from .serializers import *


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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        if post:
            post.update_views()
            serializer = self.get_serializer(post)
            return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, id=request.data['blog'])
        if blog.authors.filter(id=request.user.id).exists() or request.user.id == blog.owner.id:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
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

