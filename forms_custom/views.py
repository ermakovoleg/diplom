#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.forms import HiddenInput
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from forms_custom.forms import *
from forms_custom.models import Template
from django.forms.formsets import formset_factory
from functools import partial, wraps


@login_required(login_url='/login/', redirect_field_name=None)
def get_form(request, template):
    templ = get_object_or_404(Template, pk=template)
    rec = get_object_or_404(Record, template=templ, user=request.user, completed=False)
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
                    rec.completed = True
                    rec.save()
                    RecordData.objects.filter(record=rec).delete()
                    x = 0
                    for form in formsetdata:
                        form.save(rec, x)
                        x += 1
                    return redirect("/")
                else:
                    return render_to_response('multiform.html', {'formFactory': formsetdata, },
                                              context_instance=RequestContext(request))
            else:
                formfactory = formset()
                return render_to_response('multiform.html', {'formFactory': formfactory, },
                                          context_instance=RequestContext(request))

        else:
            if request.method == 'POST':
                sign = request.POST.get('sign', False)
                form = CustomForm(template=templ, data=request.POST)
                if form.is_valid():
                    rec.cdt = datetime.now()
                    rec.esign = sign
                    rec.completed = True
                    rec.save()
                    RecordData.objects.filter(record=rec).delete()
                    form.save(rec)
                    return redirect("/")
                else:
                    return render_to_response('form.html', {'form': form, }, context_instance=RequestContext(request))
            else:
                form = CustomForm(template=templ)
                form.fields["sign"] = forms.CharField(required=False, widget=HiddenInput)
                return render_to_response('form.html', {'form': form, }, context_instance=RequestContext(request))
