from django.contrib import admin

from .models import Thread, ChatMessage

admin.site.register(Thread)
admin.site.register(ChatMessage)
