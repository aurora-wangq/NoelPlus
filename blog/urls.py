#novel-urls
from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('select_blog', views.select_novel, name='select_blog'),
    path('blog/<int:blog_id>', views.novel, name='blog'),
    path('novel_like/<int:novel_id>', views.novel_like, name='blog_like')
]