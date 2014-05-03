from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext
from reports.models import Report, ReportMaps


def get_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    data, title = report.get_peportrecord()

    return render_to_response('report.html', {'data': data, 'title': title})


@login_required(login_url='/login/', redirect_field_name=None)
def maps(request, pk):
    report = get_object_or_404(ReportMaps, pk=pk)
    fields = report.reportrecordmaps_set.all()
    ololo = []
    for field in fields:
         ololo.append(field.get_value())
    return render_to_response('maps.html', {'data': report, 'fields': ololo}, context_instance=RequestContext(request))