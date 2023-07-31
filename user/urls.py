#user-urls
from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('user_page/', views.user_page, name='user_page'),
    path('user/<int:user_id>', views.others_page, name='others_page'),
    path('user/<int:user_id>/follow', views.follow, name='follow'),
]