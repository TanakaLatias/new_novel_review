from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Work, Scene, Poll, Post, Like, Read
from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin

class UserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email')
    ordering = ('-pk',)

class WorkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'creator')
    search_fields = ('title', 'creator')
    ordering = ('-pk',)

class SceneAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'work')
    search_fields = ('title', 'work__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class PollAdmin(admin.ModelAdmin):
    list_display = ('pk', 'scene', 'user')
    search_fields = ('scene__work__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'work', 'user', 'hide')
    search_fields = ('work__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

class LikeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'post')
    search_fields = ('user__email__icontains', 'post__work__title__icontains')
    ordering = ('-pk',)

class ReadAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'work')
    search_fields = ('work__title__icontains', 'user__email__icontains')
    ordering = ('-pk',)

admin.site.register(Work, WorkAdmin)
admin.site.register(Scene, SceneAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Read, ReadAdmin)
admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)