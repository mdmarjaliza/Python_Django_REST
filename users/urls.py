from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from users.api import SignupAPI, UserDetailAPI, BlogsListViewSet
from users.views import LoginView, LogoutView, BlogsView, SignupView

router = DefaultRouter()
router.register('api/1.0/blogs', BlogsListViewSet, base_name='api_blogs')

urlpatterns = [
    #Web URLs
    url(r'^login$', LoginView.as_view(), name='users_login'),
    url(r'^logout$', LogoutView.as_view(), name='users_logout'),
    url(r'^signup$', SignupView.as_view(), name='users_signup'),
    url(r'^blogs/$', BlogsView.as_view(), name='users_blogs'),

    #API URLs
    # url(r'^api/1.0/blogs$', BlogsListAPI.as_view(), name='api_blogslist'),
    url(r'^api/1.0/users/(?P<blogger>[a-z0-9_-]+)$', UserDetailAPI.as_view(), name='api_userdetail'),
    url(r'^api/1.0/signup$', SignupAPI.as_view(), name='api_signup'),

    url(r'', include(router.urls))
]