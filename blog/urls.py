#blog-urls
from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('<int:blog_id>/', views.blog, name='blog'),
    #path('<int:blog_id>/like/', views.ike, name='like'),
    path('<int:blog_id>/comment/', view=views.comment, name='comment'),
    path('new/', view=views.new, name='new'),
]