from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'blogs', BlogViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagsViewSet)
router.register(r'like', LikeViewSet, basename='like')
router.register(r'subscriptions', SubscriptionsViewSet, basename='subscriptions')
router.register(r'my_posts', MyPosts, basename='my_posts')
router.register(r'my_subscriptions', MySubscriptions, basename='my_subscriptions')
router.register(r'change_publish', ChangePublish, basename='change_publish')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]
