from django.contrib import admin

# Register your models here.
from .models import Blog, BlogComment,  Category, SubCategory, Subscribers, ReadArticles, CommentReply, Notification

admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Subscribers)
admin.site.register(ReadArticles)
admin.site.register(Notification)
admin.site.register(CommentReply)
