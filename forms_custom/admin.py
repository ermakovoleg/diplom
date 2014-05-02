from django.contrib import admin
from forms_custom.models import *


class TemplateFieldInline(admin.TabularInline):
    model = TemplateField
    extra = 2


class TemplateAdmin(admin.ModelAdmin):
    inlines = [TemplateFieldInline, ]
    save_as = True
    list_display = ('title', 'cdt')
    date_hierarchy = 'cdt'


class FieldParameterInline(admin.TabularInline):
    model = FieldParameter
    extra = 1


class TemplateFieldAdmin(admin.ModelAdmin):
    inlines = [FieldParameterInline, ]
    #save_as = True
    list_display = ('template', 'title', 'type')
    list_display_links = ('template', 'title', 'type')
    list_filter = ('template',)


class FieldParameterAdmin(admin.ModelAdmin):
    pass


class RecordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateField, TemplateFieldAdmin)
#admin.site.register(FieldParameter)
admin.site.register(Record)
admin.site.register(RecordData)
