#coding: utf-8
import csv
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from setuptools.compat import unicode
from forms_custom.forms import *
from forms_custom.models import Template
from django.forms.formsets import formset_factory
from functools import partial, wraps


@login_required(login_url='/login/', redirect_field_name=None)
def get_form(request, template):
    templ = get_object_or_404(Template, pk=template)
    rec = get_object_or_404(Record, template=templ, user=request.user, status__in=['W', 'K'])
    if templ.check_user(request.user):
        if templ.tableview:
            #min_num=1 в джанго 1.7
            formset = formset_factory(wraps(CustomForm)(partial(CustomForm, template=templ)), extra=3)
            if request.method == 'POST':
                sign = request.POST.get('sign', False)
                formsetdata = formset(request.POST)
                if formsetdata.is_valid():
                    rec.cdt = datetime.now()
                    rec.esign = sign
                    rec.status = 'O'
                    rec.save()
                    RecordData.objects.filter(record=rec).delete()
                    x = 0
                    for form in formsetdata:
                        form.save(rec, x)
                        x += 1
                    return redirect("/")
                else:
                    comments = rec.get_comments()
                    return render_to_response('multiform.html', {'formFactory': formsetdata,
                                                                 'template': templ,
                                                                 'comments': comments},
                                              context_instance=RequestContext(request))
            else:
                if rec.status == 'K':
                    initial = rec.data_form()
                    formfactory = formset(initial=initial)
                    comments = rec.get_comments()
                else:
                    formfactory = formset()
                    comments = None
                return render_to_response('multiform.html', {'formFactory': formfactory,
                                                             'template': templ,
                                                             'comments': comments},
                                          context_instance=RequestContext(request))

        else:
            if request.method == 'POST':
                sign = request.POST.get('sign', False)
                form = CustomForm(template=templ, data=request.POST)
                if form.is_valid():
                    rec.cdt = datetime.now()
                    rec.esign = sign
                    rec.status = 'O'
                    rec.save()
                    RecordData.objects.filter(record=rec).delete()
                    form.save(rec)
                    return redirect("/")
                else:
                    comments = rec.get_comments()
                    return render_to_response('form.html', {'form': form,
                                                            'template': templ,
                                                            'comments': comments},
                                              context_instance=RequestContext(request))
            else:
                if rec.status == 'K':
                    initial = rec.data_form()
                    form = CustomForm(template=templ, initial=initial)
                    comments = rec.get_comments()
                else:
                    form = CustomForm(template=templ)
                    comments = None
                form.fields["sign"] = forms.CharField(required=False, widget=HiddenInput)
                return render_to_response('form.html', {'form': form,
                                                        'template': templ,
                                                        'comments': comments},
                                          context_instance=RequestContext(request))
    return redirect('/')


@login_required(login_url='/login/', redirect_field_name=None)
def form_publish(request):
    templates = Template.objects.filter(publish=True)
    return render_to_response('baseadmin.html', {'templates': templates, }, context_instance=RequestContext(request))


@login_required(login_url='/login/', redirect_field_name=None)
def form_status(request, pk):
    template = get_object_or_404(Template, pk=pk)
    if request.POST:
        if 'export' in request.POST:
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=export.csv'
            writer = csv.writer(response, delimiter=';', dialect='excel')
            response.write(u'\ufeff'.encode('utf8'))
            head = [x.title for x in template.fields()]
            head1 = [x.tag for x in template.fields()]
            head.append('Пользователь')
            writer.writerow(head)
            for record in template.get_records().filter(status="R"):
                if template.tableview:
                    for line in record.data_form():
                        temp = [line[key] for key in head1]
                        temp.append(record.user.get_fio())
                        writer.writerow(temp)
                else:
                    data = record.data_form()
                    temp = [data[key] for key in data]
                    temp.append(record.user.get_fio())
                    writer.writerow(temp)
            return response
    return render_to_response('baseadmin.html', {'template': template}, context_instance=RequestContext(request))


@login_required(login_url='/login/', redirect_field_name=None)
def get_record(request, pk):
    record = get_object_or_404(Record, pk=pk)
    comments = None
    if request.POST:
        if 'export' in request.POST:
            response = HttpResponse(mimetype='text/csv')
            response['Content-Disposition'] = 'attachment; filename=export.csv'
            writer = csv.writer(response, delimiter=';', dialect='excel')
            response.write(u'\ufeff'.encode('utf8'))
            writer.writerow([x.title for x in record.template.fields()])
            if record.template.tableview:
                for line in record.data_form():
                    writer.writerow([value for key, value in line.items()])
            else:
                writer.writerow([value for key, value in record.data_form().items()])
            return response

        if 'approve' in request.POST:
            record.approved = request.user
            record.status = 'R'
            record.save()
        if 'revision' in request.POST:
            record.status = 'K'
            record.save()
            comment = request.POST.get('comment', False)
            if comment:
                comm = Comments(user=request.user, record=record, comment=comment)
                comm.save()
    else:
        comments = record.get_comments()
    return render_to_response('baseadmin.html', {'record': record,
                                                 'comments': comments,
                                                 'sign_value':record.get_sign_value()},
                              context_instance=RequestContext(request))