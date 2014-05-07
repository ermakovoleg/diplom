#coding: utf-8
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group


class District(models.Model):
    name_district = models.CharField(max_length=70, verbose_name="Название района")

    def __unicode__(self):
        return self.name_district

    class Meta:
        verbose_name = u'Район'
        verbose_name_plural = u'Районы'
        ordering = ('name_district',)


class Locality(models.Model):
    name = models.CharField(max_length=50, verbose_name="наименование населенного пункта")
    district = models.ForeignKey('District', verbose_name='район')

    def __unicode__(self):
        return self.district.name_district + " -- " + self.name

    class Meta:
        verbose_name = u'Населенный пункт'
        verbose_name_plural = u'Населенные пункты'
        ordering = ('district', 'name')


class MyUserManager(BaseUserManager):
    def create_user(self, username, locality, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            locality=locality,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    locality = models.ForeignKey('Locality', verbose_name="Населенный пункт", blank=True, null=True)
    email = models.EmailField(verbose_name='email', max_length=255)

    is_admin = models.BooleanField(default=False, verbose_name='доступ к административному интерфейсу')

    objects = MyUserManager()

    USERNAME_FIELD = "username"

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class MyGroup(models.Model):
    title = models.CharField(max_length=25, unique=True, verbose_name="наименование группы")

    def __str__(self):
        return self.title

    def get_user(self):
        return MyUser.objects.filter(pk__in=MyGroupUser.objects.filter(group=self).values('user')).order_by("username")

    class Meta:
        verbose_name = 'группа пользователей'
        verbose_name_plural = 'группы пользователей'


class MyGroupUser(models.Model):
    group = models.ForeignKey(MyGroup)
    user = models.ForeignKey(MyUser)


class GroupMeta(Group):
    class Meta:
        verbose_name = 'Права пользователей'
        verbose_name_plural = 'Права пользователей'
        proxy = True
