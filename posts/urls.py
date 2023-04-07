from django.urls import path
from . import views
urlpatterns = [
    path('upload', views.upload.as_view(), name='upload'),
    path('uploadtext', views.uploadTextPost.as_view(), name='uploadtext'),
    path('likepost', views.Like_Post.as_view(), name='like-post'),
    path('likeComment/<str:comment_id>', views.LikeComments.as_view(), name = 'likeComment'),
    path('islike', views.is_like.as_view(), name='islike'),
    path('comment/id=<str:id>/page=<int:page>', views.CommentView.as_view(), name='commentview'),
    path('comment', views.CommentView.as_view(), name='comment'),
    path('postlist/page=<int:page>', views.MyPostListView.as_view(), name='postlist'),
    path('mygallery/page=<int:page>', views.MyGallery.as_view(), name='postlist'),
    path('postview/<str:user>/page=<int:page>', views.PostView.as_view(), name="postview"),
    path('getpost/id=<str:postId>', views.GetPostDataById.as_view(), name="getpostdata"),
    path('changePrivacy/<str:id>/privacy=<str:privacy>', views.ChangePrivacy.as_view()),
    path('deletePosts/postId=<str:postId>', views.DeletePost.as_view(), name = 'deletePost'),
    path('delete_comment/commentId=<int:id>/postId=<str:postId>', views.DeleteCommentView.as_view(), name='deleteComent')
]
