from django.urls import path, include
from . import views

app_name = 'blog'  

urlpatterns = [
    path('blog/', views.blog, name='blog'),  
    path('blog_detail/<int:pk>/', views.blog_detail, name='blog_detail'),  
    path('add_comment/<int:pk>/', views.add_comment, name='add_comment'),  
    path('add_blog_post/', views.add_blog_post, name='add_blog_post'),  
]
