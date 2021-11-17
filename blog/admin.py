from django.contrib import admin

from blog.models import Blog, BlogAuthor, BlogComment

# Register your models here.
# admin.site.register(BlogAuthor)
# admin.site.register(Blog)
# admin.site.register(BlogComment) 


class BlogPostInline(admin.TabularInline):
    model = Blog
    extra = 0
    fields = ('name', 'post_date')

@admin.register(BlogAuthor)
class BlogAuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    list_filter = ('user',)
    
    inlines = [BlogPostInline]


class BlogCommentInline(admin.TabularInline):
    """Used to show 'existing' blog comments inline below associated blogs"""
    model = BlogComment
    extra = 0 

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'post_date') 
    list_filter = ('author','post_date')
   
    inlines = [BlogCommentInline]

    fieldsets = (
        ('Blog details',{
            'fields': ('author', 'name')
        }),
        ('Content details',{
            'fields': ('description', 'post_date')
        }),
    )


@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post_date')
    list_filter = ('post_date',)

    fieldsets = (
        ('Comment details',{
            'fields': ('description', 'blog')
        }),
        ('Author details',{
            'fields': ('author',)
        }),
    )