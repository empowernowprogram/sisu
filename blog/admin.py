from django.contrib import admin
from .models import Post, Comment, PostPreferrence, ReplyToComment, Cluster, Resource, PressArticle, MediumPost, LinkedinPost

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ['id', 'category_name', 'title']
    
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['id', 'post', 'user']
    
class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']
    
class ResourceAdmin(admin.ModelAdmin):
    model = Resource
    list_display = ['id', 'title','category_name']
    
# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Resource, ResourceAdmin)

admin.site.register(PostPreferrence)
admin.site.register(ReplyToComment)

admin.site.register(Cluster, ClusterAdmin)

admin.site.register(PressArticle)
admin.site.register(MediumPost)
admin.site.register(LinkedinPost)