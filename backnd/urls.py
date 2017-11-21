from django.conf.urls import url
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token

from . import views

app_name = 'backnd'
urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^verify$', verify_jwt_token, name='verify'),
    url(r'^delete$', views.delete_account, name='delete'),
    url(r'^refresh$', refresh_jwt_token),
    url(r'^blogs',views.blogs, name="blogs")
]