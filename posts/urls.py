from django.urls import path
from . import views
urlpatterns = [
    path('upload', views.upload.as_view(), name='upload'),
    path('uploadtext', views.uploadTextPost.as_view(), name='uploadtext'),
    path('likepost', views.Like_Post.as_view(), name='like-post'),
    path('islike', views.is_like.as_view(), name='islike'),
    path('postlist/page=<int:page>', views.get_post_list.as_view(), name='postlist'),
    path('mygallery/page=<int:page>', views.MyGallery.as_view(), name='postlist'),
]
