from django.contrib import admin
from reports.models import ReportRecord, Report, ReportMaps, ReportRecordMaps


class ReportRecordInLines(admin.TabularInline):
    extra = 3
    model = ReportRecord


class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportRecordInLines, ]


class ReportRecordMapsInLines(admin.TabularInline):
    extra = 1
    model = ReportRecordMaps


class ReportMapsAdmin(admin.ModelAdmin):
    inlines = [ReportRecordMapsInLines, ]

admin.site.register(Report, ReportAdmin)
admin.site.register(ReportMaps, ReportMapsAdmin)
