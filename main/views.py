from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms_custom.models import Record
from reports.models import Report


def home(request):
    if request.user.is_authenticated():
        uncompleted_records = Record.objects.filter(status__in=['W', 'K'], user=request.user)
        context = {
            'uncompleted_records': uncompleted_records,
        }
        if request.user.is_staff:
            context['report'] = Report.objects.all()
        return render_to_response('content.html', context, context_instance=RequestContext(request))

    else:
        return render_to_response('start.html', context_instance=RequestContext(request))