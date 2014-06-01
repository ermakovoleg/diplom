#coding: utf-8
from django.db.models import Max
from django.utils.translation import ugettext
from user.models import MyUser, MyGroup, MyGroupUser
from datetime import datetime
from django.db import models
from django.template.defaultfilters import date as _date


class Template(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название формы запроса")
    cdt = models.DateTimeField(verbose_name="Дата создания", default=datetime.now)
    group_user = models.ForeignKey(MyGroup, verbose_name="кому предназначается")
    tableview = models.BooleanField(default=False, verbose_name='табличный вид')
    publish = models.BooleanField(default=False, verbose_name='опубликовано')
    creator = models.ForeignKey(MyUser, editable=False)

    def fields(self):
        return TemplateField.objects.filter(template=self).order_by('tab')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    #проверка наличия пользователя в списке доступа к данной форме
    def check_user(self, user):
        return MyGroupUser.objects.filter(group=self.group_user, user=user).exists()

    def get_records(self):
        return Record.objects.filter(template=self)

    def save(self, *args, **kwargs):
        super(Template, self).save(*args, **kwargs)
        if self.publish:
            user = self.group_user.get_user()
            for u in user:
                if not Record.objects.filter(user=u, template=self).exists():
                    rec = Record(template=self, user=u, cdt=self.cdt)
                    rec.save()

    class Meta:
        verbose_name = 'форму запроса'
        verbose_name_plural = 'формы запроса'
        ordering = ('-cdt',)


class TemplateField(models.Model):

    def set_tag():
        dt = datetime.now()
        return str(dt).replace('-', '_').replace('.', '_').replace(' ', '_').replace(':', '_')

    FieldTypes = (('T', 'Текст'), ('S', 'Строка'), ('B', 'Bool'), ('E', 'E-mail'),
                  ('U', 'URL'), ('C', 'Выбор'), ('M', 'Множественный выбор'),
                  ('P', 'Точка'), ('L', 'Линия'), ('Z', 'Полигон'), ('D', 'Дата'))

    template = models.ForeignKey(Template, verbose_name="форма запроса")
    tag = models.SlugField(max_length=100, default=set_tag, editable=False)
    title = models.CharField(max_length=255, verbose_name="вопрос")
    type = models.CharField(max_length=1, choices=FieldTypes, verbose_name="тип поля")
    tab = models.IntegerField(verbose_name="порядок")
    required = models.BooleanField(default=True, verbose_name="обязательное поле")

    def __str__(self):
        return self.template.title+" - "+_date(self.template.cdt,  'd b Y H:m')+" - "+self.title

    def parameters(self):
        return FieldParameter.objects.filter(field=self)

    class Meta:
        unique_together = ("template", "tag")
        verbose_name = 'элемент формы'
        verbose_name_plural = 'элементы формы'


class FieldParameter(models.Model):
    TagTypes = (('choice', 'choice'), ('help_text', 'help_text'),)
    field = models.ForeignKey(TemplateField, verbose_name="поле")
    tag = models.SlugField(max_length=10, choices=TagTypes, verbose_name="тип дополнительного поля")
    value = models.CharField(max_length=255, verbose_name="значение")

    def __unicode__(self):
        return self.field.template.title+" - "+self.field.title+" - "+self.tag+" - "+self.value
        
    class Meta:
        unique_together = ("field", "tag", "value")
        verbose_name = 'дополнительный параметр поля'
        verbose_name_plural = 'дополнительные параметры полей'


class Record(models.Model):

    StatusTypes = (('W', 'Данные не введены'), ('R', 'Сдано'), ('O', 'На рассмотрении'), ('K', 'Доработка'))

    template = models.ForeignKey(Template, editable=False)
    cdt = models.DateTimeField(editable=False)
    user = models.ForeignKey(MyUser, editable=False)
    esign = models.CharField(max_length=2000, default=0, editable=False)
    status = models.CharField(max_length=1, choices=StatusTypes, verbose_name="статус", default='W')
    approved = models.ForeignKey(MyUser, verbose_name='утвердил', null=True, blank=True, related_name='approved')

    def get_status(self):
        if (self.status == 'W'):
            return "Данные не введены"
        elif (self.status == 'R'):
            return 'Сдано'
        elif (self.status == 'O'):
            return 'На рассмотрении'
        elif (self.status == 'K'):
            return 'Доработка'
        else:
            return "Что то еще"

    def data(self):
        rex = RecordData.objects.filter(record=self)
        if self.template.tableview:
            num_lines = rex.aggregate(Max('line'))['line__max']
            data = []
            for x in range(num_lines+1):
                data.append(rex.filter(line=x).order_by('field__tab'))
            return data
        return rex

    def data_form(self):
        rex = RecordData.objects.filter(record=self)
        if self.template.tableview:
            num_lines = rex.aggregate(Max('line'))['line__max']
            data = []
            for x in range(num_lines+1):
                line = {}
                for rec in rex.filter(line=x).order_by('field__tab'):
                    line[rec.field.tag] = rec.value
                data.append(line)
            return data
        else:
            line = {}
            for rec in rex.order_by('field__tab'):
                line[rec.field.tag] = rec.value
            return line

    def get_comments(self):
        return Comments.objects.filter(record=self).order_by('-cdt')

    def __str__(self):
        return self.user.username+'  ('+self.template.__str__()+') - '+self.cdt.strftime("%Y-%m-%d %H:%M")

    def get_sign_value(self):
        s = ''
        if self.template.tableview:
                for line in self.data():
                    temp = [value.get_value() for value in line]
        else:
            temp = [value.get_value() for value in self.data()]
        s = ''.join(temp)
        return s


class RecordData(models.Model):
    record = models.ForeignKey(Record)
    field = models.ForeignKey(TemplateField)
    line = models.IntegerField(blank=True, null=True)
    value = models.TextField()
    
    def __unicode__(self):
        return self.value + " " + self.record.__str__() + " " + self.line.__str__()

    def get_value(self):
        if self.field.type == 'M':
            return ','.join(eval(self.value))
        return self.value

    def rendered_value(self):
        if self.field.type == 'B':
            if self.value == 'True':
                return ugettext("Да")
            elif self.value == 'False':
                return ugettext("Нет")
        return self.value


class Comments(models.Model):
    user = models.ForeignKey(MyUser, verbose_name="пользователь")
    record = models.ForeignKey(Record)
    cdt = models.DateTimeField(default=datetime.now)
    comment = models.TextField()

    def __str__(self):
        return self.record.__str__() + ' ' + self.user.get_short_name()

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ('-cdt',)