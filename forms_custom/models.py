#coding: utf-8
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

    def fields(self):
        return TemplateField.objects.filter(template=self).order_by('tab')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    #проверка наличия пользователя в списке доступа к данной форме
    def check_user(self, user):
        return MyGroupUser.objects.filter(group=self.group_user, user=user).exists()

    def save(self, *args, **kwargs):
        super(Template, self).save(*args, **kwargs)
        user = self.group_user.get_user()
        for u in user:
            rec = Record(template=self, user=u)
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
                  ('P', 'Точка'), ('L', 'Линия'), ('Z', 'Полигон'))

    template = models.ForeignKey(Template, verbose_name="форма запроса")
    tag = models.SlugField(max_length=100, default=set_tag, editable=False)
    title = models.CharField(max_length=255, verbose_name="вопрос")
    type = models.CharField(max_length=1, choices=FieldTypes, verbose_name="тип поля")
    tab = models.IntegerField(default=999, verbose_name="порядок")
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
    template = models.ForeignKey(Template)
    cdt = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(MyUser)
    esign = models.CharField(max_length=2000, default='')
    completed = models.BooleanField(verbose_name='завершено', default=False)

    def __unicode__(self):
        return self.cdt.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.user.username+'  '+self.cdt.strftime("%Y-%m-%d %H:%M:%S")
        
    def data(self):
        return RecordData.objects.filter(record=self).order_by('field__tab')


class RecordData(models.Model):
    record = models.ForeignKey(Record)
    field = models.ForeignKey(TemplateField)
    value = models.TextField()
    
    def __unicode__(self):
        return str(self.record)+" - "+str(self.field)

    def __str__(self):
        return self.value

    def decoded_value(self):
        if self.field.type == 'M':
            return eval(self.value)
        return self.value

    def rendered_value(self):
        if self.field.type == 'B':
            if self.value == 'True':
                return ugettext("Да")
            elif self.value == 'False':
                return ugettext("Нет")
        return self.value