from django.contrib import admin

# Register your models here.
from .models import Comment, Review


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('buyer',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller')
