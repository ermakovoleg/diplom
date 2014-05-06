from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import get_script_prefix
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import iri_to_uri, python_2_unicode_compatible

@python_2_unicode_compatible
class FlatPage(models.Model):
    url = models.CharField(verbose_name='URL', max_length=100, db_index=True)
    title = models.CharField(verbose_name='Заголовок', max_length=200)
    content = models.TextField(verbose_name='Контент', blank=True)
    template_name = models.CharField(verbose_name='Имя шаблона', max_length=70, blank=True,
                                     help_text=_("Пример: 'flatpages/contact_page.html'. "
                                                 "Стандартное значение 'flatpages/default.html'."))
    registration_required = models.BooleanField(
        verbose_name='Доступ к странице только зарегистрированным пользователям', default=False)

    class Meta:
        verbose_name = 'Простая страница'
        verbose_name_plural = 'Простые страницы'
        ordering = ('url',)

    def __str__(self):
        return "%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        # Handle script prefix manually because we bypass reverse()
        return iri_to_uri(get_script_prefix().rstrip('/') + self.url)
