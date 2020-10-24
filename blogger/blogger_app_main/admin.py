from django.contrib import admin
from .models import Blog,Post,Read,Follow
# Register your models here.
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Read)
admin.site.register(Follow)