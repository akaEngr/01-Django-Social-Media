from django.urls import path
from . import views
urlpatterns = [
    path('', views.user_profile, name='user_profile'),
    path('user_post/', views.user_post, name='user_post'),
    path('showdata_profile_post/', views.showdata_profile_post, name='showdata_profile_post'),
    path('showdata_post_tags/', views.showdata_post_tags, name='showdata_post_tags'),
    # path('show_post_likes/', views.show_post_likes, name='show_post_likes'),
    path('show_post_comment/', views.show_post_comment, name='show_post_comment'),
    path('methodspractice/', views.methodspractice, name='methodspractice'),
]

