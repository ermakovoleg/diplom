from django.db import models
from user.models import MyGroup
from forms_custom.models import TemplateField,Record,RecordData


class Report(models.Model):
    title = models.CharField(max_length=120, verbose_name="Наименование отчета")
    user_group = models.ForeignKey(MyGroup, verbose_name="Группа???")
    transp = models.BooleanField(verbose_name='транспонировать')

    def __str__(self):
        return self.title

    def get_peportrecord(self):
        user = self.user_group.get_user()
        record = Record.objects.filter(user__in=user)
        templField = ReportRecord.objects.filter(report=self)

        data = RecordData.objects.filter(record__in=record, field__in=templField.values('field'))

        data = [{'record': x.field.title, 'value': x.value, 'user': x.record.user.username}for x in data]

        m1 = [u.username for u in list(user)]
        m2 = [r.field.title for r in templField]


        data1 = []
        for i, u in enumerate(m1):
            data1.append([])
            for j, r in enumerate(m2):
                x = False
                for d in data:
                    if (u == d.get('user')) and (r == d.get('record')):
                        x = d.get('value')
                        continue
                data1[i].append(x)

        if self.transp:

            print(m2)
            data1 = list(zip(*data1))
            for i, k in enumerate(data1):
                data1[i] = [m2[i]]+list(data1[i])
            title = m1
        else:
            for i, k in enumerate(data1):
                data1[i] = [m1[i]]+data1[i]
            title = m2

        return data1, title


class ReportRecord(models.Model):
    report = models.ForeignKey(Report)
    field = models.ForeignKey(TemplateField)