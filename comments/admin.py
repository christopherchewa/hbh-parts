from django.contrib import admin

# Register your models here.
from .models import Comment, Review


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'property_entry', 'get_comment')


admin.site.register(Review)