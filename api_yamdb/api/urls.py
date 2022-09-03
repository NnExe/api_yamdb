from django.urls import include, path
from rest_framework import routers

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, user_me,
                       user_signup, user_token)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register(r'^users', UserViewSet, basename='users')
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

auth_patterns = [
    path('signup/', user_signup, name='user_signup'),
    path('token/', user_token, name='user_token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/users/me/', user_me, name='user_me'),
    path('v1/', include(router_v1.urls)),
]
