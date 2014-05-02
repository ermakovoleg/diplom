from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms_custom.models import Record
from reports.models import Report


@login_required(login_url='/login/', redirect_field_name=None)
def home(request):
    uncompleted_records = Record.objects.filter(completed=False, user=request.user)
    print(uncompleted_records)
    context = {
        'uncompleted_records': uncompleted_records,
    }
    if request.user.is_staff:
        context['report'] = Report.objects.all()
    return render_to_response('content.html', context, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def home1(request):
    return render_to_response('base.html', {}, context_instance=RequestContext(request))