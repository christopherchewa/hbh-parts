from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (User, 
    UserProfile, 
    PropertyEntry, 
    PropertyEntryImage, 
    Request, 
    Response, 
    Favourite,
    Match)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)



@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_type')

class PropertyEntryImageInline(admin.TabularInline):
    model = PropertyEntryImage


@admin.register(PropertyEntry)
class PropertyEntryAdmin(admin.ModelAdmin):
    inlines = [PropertyEntryImageInline]
    list_display = ('__str__','is_available', )

@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'get_favourites')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('buyer_request', 'is_valid')


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active')



admin.site.register(Response)
