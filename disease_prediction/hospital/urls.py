from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.signout, name='logout'),
    path('test', views.test, name='test'),
    path('home', views.home, name='home'),
    path('test_result', views.test_result, name='test_result'),
    
]