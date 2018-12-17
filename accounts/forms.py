# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth


# 登录表单验证
class LoginForm(forms.Form):
    username = forms.CharField(label=u'账 号', error_messages={'required': u'99999'},
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=u'密 码', error_messages={'required': u'密码不能为空'},
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user_cache = None

        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'用户不存在或密码错误')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
