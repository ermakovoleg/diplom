# codind utf-8
from datetime import datetime
from django import forms
from django.forms.formsets import BaseFormSet
from suit.widgets import AutosizedTextarea
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
                                                            widget=forms.CheckboxInput(attrs={'class': 'my-form', 'style': 'min-width:50px'}))
            elif field.type == "S":
                if widget == None:
                    widget = forms.TextInput(attrs={'class': 'my-form'})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

            elif field.type == "T":
                if widget == None:
                    #widget = forms.Textarea(attrs={'class': 'my-form'})
                    widget = AutosizedTextarea(attrs={'class': 'my-form'})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

            elif field.type == "C":
                choices = [('', '-')]
                for parameter in field.parameters():
                    if parameter.tag == "choice":
                        choices.append((parameter.value, parameter.value))
                widget = forms.Select(attrs={'class': 'my-form'})
                self.fields[field.tag] = forms.ChoiceField(choices=choices,
                                                           help_text=help_text,
                                                           label=field.title,
                                                           widget=widget)
            elif field.type == "M":
                choices = []
                for parameter in field.parameters():
                    if parameter.tag == "choice":
                        choices.append((parameter.value, parameter.value))
                widget = forms.SelectMultiple(
                    attrs={'class': 'my-form', 'multiple': ''})
                self.fields[field.tag] = forms.MultipleChoiceField(choices=choices,
                                                                   help_text=help_text,
                                                                   label=field.title,
                                                                   widget=widget,
                                                                   required=False)
            elif field.type == "E":
                widget = forms.EmailInput(attrs={'class': 'my-form'})
                self.fields[field.tag] = forms.EmailField(label=field.title,
                                                          help_text=help_text,
                                                          required=field.required,
                                                          widget=widget)
            elif field.type == "U":
                widget = forms.URLInput(attrs={'class': 'my-form'})
                self.fields[field.tag] = forms.URLField(label=field.title,
                                                        required=field.required,
                                                        help_text=help_text,
                                                        widget=widget)
            elif field.type == "P":
                if widget == None:
                    widget = forms.TextInput(attrs={'class': 'my-form',
                                                    'onclick': "openmap('P',this); input=this;",
                                                    "data-toggle": "modal",
                                                    "data-target": "#myModal"})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

            elif field.type == "L":
                if widget == None:
                    widget = forms.TextInput(attrs={'class': 'my-form',
                                                    'onclick': "openmap('L',this); input=this;",
                                                    "data-toggle": "modal",
                                                    "data-target": "#myModal"})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

            elif field.type == "Z":
                if widget == None:
                    widget = forms.TextInput(attrs={'class': 'my-form',
                                                    'onclick': "openmap('Z',this); input=this;",
                                                    "data-toggle": "modal",
                                                    "data-target": "#myModal"})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)
            elif field.type == "D":
                widget = forms.DateInput(attrs={'class': 'my-form', 'type': 'date'})
                self.fields[field.tag] = forms.CharField(label=field.title,
                                                         required=field.required,
                                                         help_text=help_text,
                                                         widget=widget)

    def save(self, record, i=None):
        data = self.cleaned_data
        for k in data:
            f = TemplateField.objects.get(template=self.template, tag=k)
            d = RecordData(record=record, field=f, line=i, value=('%s' % data[k]))
            d.save()
        return record