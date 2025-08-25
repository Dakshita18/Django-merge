from django.contrib import admin
from .models import Post,User,Tag,Category,Comment

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment)
