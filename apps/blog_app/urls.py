from django.urls import path

from apps.blog_app.views import BlogPostListView, BlogPostDetailView

app_name = 'blog_app'

urlpatterns = [
    path('', BlogPostListView.as_view(
        template_name='blog_app/blogpost_list.html'
    ), name='post_list'),
    path('post/<slug:slug>/', BlogPostDetailView.as_view(
        template_name='blog_app/blogpost_detail.html'
    ), name='post_detail'),
]
