from django.contrib import admin
from .models import Blog

class blogdisplay(admin.ModelAdmin):
    list_display = ('title','author','time')

admin.site.register(Blog,blogdisplay)