from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.my, name='my'),
    path('register/',views.register, name='register'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('edit/', views.edit, name='edit'),
    path('<int:target_id>/', views.user, name='user'),
    path('<int:target_id>/follow', views.follow, name='follow'),
]