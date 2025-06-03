from django.contrib import admin

from django.contrib import admin
from .models import User, Pet, Post, Comment, Like, Friendship, Message

admin.site.register(User)
admin.site.register(Pet)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Friendship)
admin.site.register(Message)

