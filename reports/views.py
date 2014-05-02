from django.shortcuts import render, get_object_or_404, render_to_response
from reports.models import Report


def get_report(request, pk):
    report = get_object_or_404(Report, pk=pk)
    data, title = report.get_peportrecord()

    return render_to_response('report.html', {'data': data, 'title': title})