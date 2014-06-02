from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from reports.models import Report, ReportMaps


def get_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    data, title = report.get_peportrecord()

    return render_to_response('report.html', {'data': data, 'title': title, 'report': report},
                              context_instance=RequestContext(request))


def get_reports(request):
    reports = Report.objects.all()
    reports_map = ReportMaps.objects.all()
    return render_to_response('reports.html', {'reports': reports, 'reports_map': reports_map},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/', redirect_field_name=None)
def maps(request, pk):
    report = get_object_or_404(ReportMaps, pk=pk)
    fields = report.reportrecordmaps_set.all()
    records = []
    for field in fields:
        records.append(field.get_value())
    context = {
        'report': report,
        'records': records
    }
    return render_to_response('maps.html', context, context_instance=RequestContext(request))

