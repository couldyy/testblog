from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

# Register your models here.

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title', 'created_at', 'updated_at', 'posted_by', 'get_photo', 'views', 'category')
    list_display_links = ('slug', 'title')
    list_filter = ('category', 'tag')
    fields = ('title', 'slug', 'content', 'photo', 'get_photo', 'created_at', 'posted_by', 'category', 'views', 'tag')
    readonly_fields = ('views', 'created_at', 'get_photo')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe((f'<img src="{obj.photo.url}" width=75>'))

    get_photo.short_description = 'Миниатюра'

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title')
    list_display_links = ('slug', 'title')

class TagsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'title')
    list_display_links = ('slug', 'title')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_created_comment', 'comment_content', 'post_of_comment', 'comm_to_repl', 'like_count')
    list_display_links = ('user_created_comment', 'comment_content', 'post_of_comment', 'comm_to_repl', 'like_count')
    fields = ('user_created_comment', 'comment_content', 'post_of_comment', 'comm_to_repl', 'like_count', 'likes')




admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Comment, CommentAdmin)