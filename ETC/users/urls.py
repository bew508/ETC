from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('list', views.list, name='list'),
    path('createaccount', views.create_account, name='create_account'),
    path('remove', views.remove, name='remove'),
]
