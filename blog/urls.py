from django.urls import path

from .views import BlogPostListAPIView, DetailBlogPostAPIView


app_name = 'blog'

urlpatterns = [
    path('posts/', BlogPostListAPIView.as_view(), name='list'),
    path('posts/<int:pk>/', DetailBlogPostAPIView.as_view(), name='detail'),

]
