from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from . import views

app_name = 'backnd'

auth_urls = [
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^verify$', verify_jwt_token),
	url(r'^delete$', views.delete_account, name='delete'),
	url(r'^refresh$', refresh_jwt_token),
]

blog_urls = [
	url(r'^blogs',views.blogs, name="blogs"),
	url(r'^user',views.user, name="user"),
	url(r'^newPost',views.newPost, name="newPost"),
	url(r'^(?P<username>[a-z0-9.]+)/$',views.author, name="author"),
]

urlpatterns = auth_urls + blog_urls