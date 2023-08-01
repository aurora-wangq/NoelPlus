#NoelPlus-urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('zone.urls')),
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('chat/',include('chat.urls')),
    path('blog/',include('blog.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.THUMBNAIL_URL, document_root=settings.THUMBNAIL_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)