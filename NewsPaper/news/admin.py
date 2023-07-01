# from django.contrib import admin

from django.contrib import admin
from .models import Post, Category, PostCategory, Comment, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'postTitle', 'categoryType', 'postText', 'datetimeCreation', 'postRating', 'author_id', 'get_username']
    # list_display = [field.name for field in Post._meta.get_fields()]
    list_display.append('get_category')
    list_filter = ['postTitle', 'categoryType', 'datetimeCreation', 'postRating', 'author_id']
    search_fields = ['postTitle', 'categoryType', 'datetimeCreation']
    list_editable = ('categoryType', )

    def get_category(self, obj):
        return ", ".join([p.name for p in obj.postCategory.all()])

    def get_username(self, obj):
        result = Author.objects.filter(post=obj).values('authorUser')
        return result


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    list_filter = ['post', 'category']
    search_fields = ['post', 'category']


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'authorUser', 'authorRating']
    list_filter = ['authorUser', 'authorRating']
    search_fields = ['authorUser']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
