from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        data = {"name": request.user}
        return render(request, 'index.html', locals())
