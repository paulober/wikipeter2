from django.contrib import admin
from .models import ClassCategory, Post, Class, MasterCategory, WikiFile, WikiPostFile

# Register your models here.

# Posts will be accessible from the admin area
admin.site.register(Post)
admin.site.register(Class)
admin.site.register(ClassCategory)
admin.site.register(MasterCategory)
admin.site.register(WikiFile)
admin.site.register(WikiPostFile)
