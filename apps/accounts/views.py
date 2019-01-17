from django.shortcuts import render
from django.views.generic.base import View
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm
from . import models


# Create your views here.


class LoginView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            kwargs = {
                'request': request,
                'login_form': LoginForm(),
                'redirect_url': "/",
            }
            return render(request, 'accounts/login.html', kwargs)
        else:
            return HttpResponseRedirect('/')

    def post(self, request):
        redirect_to = request.GET.get('next', '/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = request.POST['username']
            pass_word = request.POST['password']
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg'] = '用户未激活！'
            else:
                ret['msg'] = '用户名或密码错误！'
        else:
            ret['msg'] = '用户和密码不能为空！'
        kwargs = {
                'request': request,
                'login_form': login_form,
                'redirect_url': redirect_to,
            }
        return render(request, 'accounts/login.html', kwargs)


class LogoutView(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class UserListView(generic.ListView):
    model = models.UserInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dd=[field for field in models.UserInfo._meta.get_fields()]
        context["filed_name"]=dd
        for i in dd:
            print(i)
        return context


class UserCreateView(generic.CreateView):
    model = models.UserInfo
    template_name = "value_create.html"
    fields = ('username', 'password', 'email', 'work_phone', 'visa_status', 'visa_issue_date', 'visa_expir_date', 'entry_date',
               'rfid', 'rfid_name', 'is_active', 'is_superuser', )

    def get_form(self, form_class=None):
        form = super().get_form()
        return form


class UserDetailView(generic.DetailView):
    model = models.UserInfo
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # gghh = [(field.name, field.value_to_string(object)) for field in models.CustomUser._meta.fields]
        # # context["fil_name"] = serializers.serialize('python', models.CustomUser.objects.all())
        # context["fil_name"]=gghh
        print(context)
        return context


class UserUpdateView( generic.UpdateView):
    model = models.UserInfo
    template_name = 'value_update.html'
    fields = ('username', 'email', 'work_phone', 'visa_status', 'visa_issue_date', 'visa_expir_date', 'entry_date',
               'rfid', 'rfid_name', 'is_active', 'is_superuser',)
    pk_url_kwarg = 'id'

    def get_form(self, form_class=None):
        form = super().get_form()
        form.fields['username'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        return form
