from django.contrib import admin
from django.forms import ModelForm, TextInput
from reports.models import ReportRecord, Report, ReportMaps, ReportRecordMaps
from suit.widgets import AutosizedTextarea



class ReportRecordInLines(admin.TabularInline):
    extra = 3
    model = ReportRecord


class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportRecordInLines, ]


class ReportRecordMapsForm(ModelForm):
    class Meta:
        widgets = {
            'parametrs': AutosizedTextarea
        }


class ReportRecordMapsInLines(admin.TabularInline):
    extra = 1
    model = ReportRecordMaps
    form = ReportRecordMapsForm


class ReportMapsAdmin(admin.ModelAdmin):
    inlines = [ReportRecordMapsInLines, ]

    suit_form_includes = (
        ('admin/help_map_report.html', 'bottom', ''),
    )

    class Media:
        # edit this path to wherever
        css = {'all': ('css/no-addanother-button.css',)}

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportMaps, ReportMapsAdmin)
