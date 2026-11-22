from django.contrib import admin
from .models import Thread, Post, Message

admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Message)