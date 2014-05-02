#codind utf-8
from datetime import datetime
from django import forms
from django.forms.formsets import BaseFormSet
from forms_custom.models import *


class CustomForm(forms.Form):
    def __init__(self, template=None, url=None, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        if template:
            self.template = template
        elif url:
            self.template = Template.objects.get(url=url)

        self.__name__ = "form"

        fields = self.template.fields()

        for field in fields:
            widget = None
            help_text = ""

            for parameter in field.parameters():
                if parameter.tag == "help_text":
                    help_text = parameter.value

            if field.type == "B":
                self.fields[field.tag] = forms.BooleanField(label=field.title,
                                                            required=False,
                                                            help_text=help_text,
                                                            widget=forms.CheckboxInput(attrs={'class': 'form-control'}))
            elif field.type == "S":
                if widget == None:
                    widget = forms.TextInput(attrs={'class': 'form-control'})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

            elif field.type == "T":
                if widget == None:
                    widget = forms.Textarea(attrs={'class': 'form-control'})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

            elif field.type == "C":
                choices = [('', '-')]
                for parameter in field.parameters():
                    if parameter.tag == "choice":
                        choices.append((parameter.value, parameter.value))
                self.fields[field.tag] = forms.ChoiceField(choices=choices,
                                                           help_text=help_text,
                                                           label=field.title,
                                                           attrs={'class': 'form-control'})
            elif field.type == "M":
                choices = []
                for parameter in field.parameters():
                    if parameter.tag == "choice":
                        choices.append((parameter.value, parameter.value))
                widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-control'})
                self.fields[field.tag] = forms.MultipleChoiceField(choices=choices,
                                                                   help_text=help_text,
                                                                   label=field.title,
                                                                   widget=widget,
                                                                   required=False)
            elif field.type == "E":
                self.fields[field.tag] = forms.EmailField(label=field.title,
                                                          help_text=help_text,
                                                          required=field.required,
                                                          attrs={'class': 'form-control'})
            elif field.type == "U":
                widget = forms.TextInput(attrs={'class': 'form-control'})
                self.fields[field.tag] = forms.URLField(label=field.title,
                                                        required=field.required,
                                                        help_text=help_text,
                                                        widget=widget)

    def save(self, record, commit=True):
        data = self.cleaned_data
        for k in data:
            f = TemplateField.objects.get(template=self.template, tag=k)
            d = RecordData(record=record, field=f, value=('%s' % data[k]))
            d.save()
        return record