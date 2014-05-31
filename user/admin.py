#coding: utf-8
from django.forms import ModelForm, SelectMultiple
from user.models import MyUser, Locality, District, MyGroupUser, MyGroup, GroupMeta

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AdminPasswordChangeForm


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'locality', 'email')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ['username', 'locality', 'email', 'is_superuser']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    change_user_password_template = 'admin/password_change_password_form.html'

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.

    list_display = ('fio', 'username', 'locality', 'email', 'is_superuser')
    list_filter = ('is_superuser', 'locality', 'fio')
    search_fields = ('email', 'username', 'fio')
    ordering = ('fio', 'email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('fio', 'email', 'locality')}),
        ('Права пользователя', {'fields': ('is_admin', 'is_superuser', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fio', 'locality', 'email', 'password1', 'password2')}
        ),
    )


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name_district',)


class LocalityAdmin(admin.ModelAdmin):
    list_display = ('district', 'name')
    list_display_links = ('district', 'name')
    list_filter = ('district',)
    search_fields = ('name',)


class MyGroupUserInLine(admin.TabularInline):
    model = MyGroupUser


class MyGroupAdmin(admin.ModelAdmin):
    inlines = [MyGroupUserInLine, ]

    class Media:
        # edit this path to wherever
        css = {'all': ('css/no-addanother-button.css',)}


class GroupMetaForm(ModelForm):
    class Meta:
        widgets = {
            'permissions': SelectMultiple(attrs={'style': 'height: 200px; width: 400px', })
        }


class GroupMetaAdmin(admin.ModelAdmin):
    form = GroupMetaForm

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(MyGroup, MyGroupAdmin)
admin.site.unregister(Group)
admin.site.register(GroupMeta, GroupMetaAdmin)
