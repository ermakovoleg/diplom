from django.contrib import admin
from reports.models import ReportRecord, Report


class ReportRecordInLines(admin.TabularInline):
    extra = 3
    model = ReportRecord


class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportRecordInLines, ]

admin.site.register(Report, ReportAdmin)
