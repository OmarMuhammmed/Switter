from django.contrib import admin
from .models import Post, Comment, ReplyComment, Reaction


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Reaction)

