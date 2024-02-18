from django.urls import path
from content.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('getContent/', getContent),
    path('userDetail/', userDetail),
    path('content/', content),
    path('updateContent/', updateContent),
    path('deleteContent/', deleteContent),
    path('searchContent/', searchContent),
]
