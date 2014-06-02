#coding: utf-8
from django import forms
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib import auth
from django.template import RequestContext
from user.models import MyUser
from django.contrib.auth.forms import PasswordChangeForm
#from django.contrib.auth.views import password_reset


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        logout(request)
        username = form.cleaned_data.get('username', None)
        password = form.cleaned_data.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('/')
        else:
            return render_to_response('auth.html',
                                      {'form': form, 'error': "Не соответствие пары логин/пароль"},
                                      context_instance=RequestContext(request))
    return render_to_response('auth.html', {'form': form, }, context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('/login/')


class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(MyPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})


def get_user(request):
    #active_users = MyUser._default_manager.filter(email__iexact=email, is_active=True)
    context = {}
    if request.method == 'POST':
        if 'change_psw' in request.POST:
            form = MyPasswordChangeForm(request.user)
            context['form'] = form
        else:
            form = MyPasswordChangeForm(request.POST)
            #if form.is_valid():

    #user = get_object_or_404(MyUser, pk=request.user.pk)
    return render_to_response('user.html', context, context_instance=RequestContext(request))


def change_password(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        logout(request)
        username = form.cleaned_data.get('username', None)
        password = form.cleaned_data.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return redirect('/')
        else:
            return render_to_response('auth.html',
                                      {'form': form, 'error': "Не соответствие пары логин/пароль"},
                                      context_instance=RequestContext(request))
    return render_to_response('auth.html', {'form': form, }, context_instance=RequestContext(request))




