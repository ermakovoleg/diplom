# -*- coding: utf-8 -*-
from django.contrib import admin
from django.forms import ModelForm
from suit_redactor.widgets import RedactorWidget
from flatpages.models import FlatPage


class FlatPageForm(ModelForm):
    class Meta:
        widgets = {
            'content': RedactorWidget(editor_options={'lang': 'ru'})
        }


class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content')}),
        ('Дополнительные опции', {'classes': ('collapse',), 'fields': ('registration_required', 'template_name')}),
    )
    list_display = ('url', 'title')
    list_filter = ('registration_required',)
    search_fields = ('url', 'title')


admin.site.register(FlatPage, FlatPageAdmin)
