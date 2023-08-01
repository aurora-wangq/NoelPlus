#zone-urls
from django.urls import path
from . import views
app_name = 'zone'
urlpatterns = [
    path('', views.home, name='home'),  
    path('edit_post/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>', views.post, name='post'),
    path('post/<int:post_id>/like', views.post_like, name='post_like'),
    path('post/<int:post_id>/comment', views.comment, name='comment'),
]