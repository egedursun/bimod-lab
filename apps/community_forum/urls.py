from django.urls import path
from . import views
from .views import LikeCommentView

app_name = 'community_forum'

urlpatterns = [
    path('categories/', views.ForumCategoryListView.as_view(
        template_name='community_forum/category_list.html'), name='category_list'),
    path('category/<slug:slug>/', views.ForumThreadListView.as_view(
        template_name='community_forum/thread_list.html'
    ), name='thread_list'),
    path('thread/<int:thread_id>/', views.ForumThreadDetailView.as_view(
        template_name='community_forum/thread_detail.html'
    ), name='thread_detail'),
    path('thread/<int:thread_id>/create_post/', views.ForumPostCreateView.as_view(
        template_name='community_forum/post_create.html'
    ), name='post_create'),
    path('post/<int:post_id>/verify_comment/<int:comment_id>/', views.ForumVerifyCommentView.as_view(),
         name='verify_comment'),
    path('comment/<int:comment_id>/like/', LikeCommentView.as_view(), name='like_comment'),
]
