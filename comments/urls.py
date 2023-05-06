from django.urls import path
from . import views

urlpatterns = [
    path('comment/id=<str:id>/page=<int:page>', views.CommentView.as_view(), name='commentview'),
    path('comment', views.CommentView.as_view(), name='comment'),
    path('sendComment/commentType=<str:commentType>', views.SendComment.as_view(), name="sendComment")
]