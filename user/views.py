#coding: utf-8
from django import forms
from django.contrib.auth import logout
from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template import RequestContext


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


def logout_view(request):
    logout(request)
    return redirect('/login/')