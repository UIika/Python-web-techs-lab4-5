from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieListView.as_view(), name='home'),
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
