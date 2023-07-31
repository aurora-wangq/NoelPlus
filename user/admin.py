from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (                    
            'Profile', 
            {
                'fields': (
                    'nickname',
                    'description',
                    'background_image',
                    'avatar',
                    'title',
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)