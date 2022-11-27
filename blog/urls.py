from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('category/<str:slug>/', cache_page(60)(GetCategory.as_view()), name='category'),
    path('post/<str:slug>/', cache_page(60)(ShowSingleNews.as_view()), name='single_news'),
    path('tag/<str:slug>/', cache_page(60)(GetNewsByTag.as_view()), name='news_by_tag'),
    path('search/', Search.as_view(), name='search'),
    path('registration/', registration, name='registration'),
    path('login/', loginn, name='login'),
    path('logout/', logoutt, name='logout'),
    path('post/<str:slug>/like/<int:comment_id>', like, name='like_comment')
]