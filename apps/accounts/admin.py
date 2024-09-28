from django import forms

from django.contrib.auth import admin as user_admin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class UserCreationPopupForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password',)


@admin.register(User)
class UserAdmin(user_admin.UserAdmin):
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'is_verified',
            )
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ("groups", "user_permissions",)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    add_popup_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'is_verified',
            ),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

    def get_fieldsets(self, request, obj=None):
        if request.GET.get('_popup') == '1':
            return self.add_popup_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """
        defaults = {}
        if obj is None:
            defaults["form"] = self.add_form
        if request.GET.get('_popup') == '1':
            defaults["form"] = UserCreationPopupForm

        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)
