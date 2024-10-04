from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet,
                    AdminCreateUserView, CustomTokenObtainView, UserSignupView)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'titles', TitleViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserSignupView.as_view(), name='signup'),
    path(
        'v1/auth/token/',
        CustomTokenObtainView.as_view(),
        name='token_obtain_pair'),
    path(
        'auth/admin/create/',
        AdminCreateUserView.as_view(),
        name='admin_create_user'),
]
