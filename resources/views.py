from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from django.urls import resolve
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views import View

from guardian.mixins import PermissionRequiredMixin, PermissionListMixin
from guardian.shortcuts import assign_perm

from . import models
from . import forms
# from .tasks import dns_test, dns_pull
from core.models import Tree


# Create your views here.
# def ResourceLogCreate(log_type, msg=None, resources=None, user=None, request=None):
#     event = EventLog()
#     event.name = log_type
#     event.event_type = log_type
#     event.detail = request
#     event.memo = msg
#     event.user = user
#     event.resources = resources
#     event.save()


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class ResourceLogListView(generic.ListView):
    model = models.EventLog
    context_object_name = 'data'

    def get(self, request, *args, **kwargs):
        obj = self.get_queryset().filter(resource=request.get())
        return obj


class ResourceListView(PermissionListMixin, generic.ListView):
    model = models.Resource
    permission_required = ['view_resource', ]
    data = None
    classification_id = None

    def get(self, request, *args, **kwargs):
        self.data = self.get_queryset()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = self.data
        context['classification_id'] = self.classification_id
        return context


class ResourceTypeListView(ResourceListView, generic.ListView):
    def get(self, request, *args, **kwargs):
        if "id" in self.kwargs:
            classification_node = Tree.objects.get_leaves(self.kwargs["id"])
            classification_node_list = [i.node for i in classification_node]
            self.data = self.get_queryset().all().filter(resource_type_id__in=classification_node_list)
            self.classification_id = self.kwargs["id"]
        return super().get(request, *args, **kwargs)


class ResourceCreateView(PermissionRequiredMixin, generic.CreateView):
    model = models.Resource
    permission_object = None
    permission_required = ['add_resource']
    template_name = "value_create.html"
    form_class = forms.ResourceForm
    pk_url_kwarg = 'id'

    def get_form(self, form_class=None, **kwargs):
        form = super().get_form()
        if "id" in self.kwargs:
            if Tree.objects.get_child(self.kwargs["id"]):
                resource_type = Tree.objects.get_child(self.kwargs["id"])
            else:
                resource_type = Tree.objects.filter(node=self.kwargs["id"])
            form.fields['resource_type'].queryset = resource_type
        else:
            form.fields['resource_type'].queryset = Tree.objects.get_leaves(1098040201000000)
        form.fields['group'].queryset = Tree.objects.get_leaves(1001010000000000)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "id" in self.kwargs:
            type_id = self.kwargs["id"]
            type_name = str(Tree.objects.get(node=type_id))
            type_form = getattr(forms, type_name + 'Form')
            if self.request.method == 'POST':
                ext_form = type_form(self.request.POST, prefix='ExtType')
            else:
                ext_form = type_form(prefix='ExtType')
        else:
            ext_form = None
        context['ext_form'] = ext_form
        return context

    def form_valid(self, form):
        resource = form.save()
        context = self.get_context_data()
        if context['ext_form'] is not None:
            ext_object = context['ext_form'].save(commit=False)
            ext_object.resource = resource
            ext_object.save()
            assign_perm('resources.view_resource', self.request.user, resource)
            assign_perm('resources.change_resource', self.request.user, resource)
            assign_perm('resources.delete_resource', self.request.user, resource)
        # dns_pull.delay("ddosroute.com")
        return super().form_valid(form)


class ResourceDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = models.Resource
    permission_required = ['view_resource', 'delete_resource']
    success_url = reverse_lazy('resource:ResourceList')


class ResourceDetailView(PermissionRequiredMixin, generic.DetailView):
    model = models.Resource
    permission_required = ['view_resource']
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        print(request,args,kwargs)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if str(self.object.resource_type) in ['d','f',]:
            print("111")
            context["collect_message"] = True
        print(context)
        return context


class ResourceUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = models.Resource
    permission_required = ['view_resource', 'change_resource']
    template_name = 'value_update.html'
    fields = '__all__'
    pk_url_kwarg = 'id'

    def get_form(self, form_class=None, **kwargs):
        form = super().get_form()
        form.fields['resource_type'].queryset = Tree.objects.get_leaves(1098040000000000)
        form.fields['group'].queryset = Tree.objects.get_leaves(1001010000000000)
        return form

    def get_context_data(self, **kwargs):
        # model 名称与 form 名称是根据资源类别建立的，需要判定是否属于合法范围
        context = super().get_context_data(**kwargs)
        obj_type = self.object.resource_type
        type_id = obj_type.node if obj_type.parent_id == 1098040300000000 else obj_type.parent_id
        type_name = str(Tree.objects.get(node=type_id))
        type_model = getattr(models, type_name) if hasattr(models, type_name) else None
        type_form = getattr(forms, type_name + 'Form') if hasattr(forms, type_name + 'Form') else None
        if type_model and type_form:
            try:
                type_annex = type_model.objects.get(resource=self.object)
                if self.request.method == 'POST':
                    ext_form = type_form(self.request.POST, instance=type_annex, prefix='ExtForm')
                else:
                    ext_form = type_form(instance=type_annex, prefix='ExtForm')
            except type_model.DoesNotExist:
                if self.request.method == 'POST':
                    ext_form = type_form(self.request.POST, prefix='ExtForm')
                else:
                    ext_form = type_form(prefix='ExtForm')
        else:
            ext_form = None
        context['ext_form'] = ext_form
        return context

    def form_valid(self, form):
        resource = form.save()
        context = self.get_context_data()
        if context['ext_form'] is not None:
            ext_object = context['ext_form'].save(commit=False)
            try:
                ext_object.resource = resource
            except Exception as e:
                print(e)
            finally:
                context['ext_form'].save()
            print(resource.resource_type_id, ext_object.name)
            if resource.resource_type_id == 1098040301010000:
                print("ddd")
                # dns_pull.delay(str(ext_object.name))
        return super().form_valid(form)


class PartnerListView(PermissionListMixin, generic.ListView):
    model = models.Partner
    permission_required = ['view_partner', ]


class PartnerCreateView(PermissionRequiredMixin, generic.CreateView):
    model = models.Partner
    permission_object = None
    permission_required = ['add_partner']
    template_name = "value_create.html"
    fields = '__all__'

    def form_valid(self, form):
        resp = super().form_valid(form)
        assign_perm('Partner.view_partner', self.request.user, self.object)
        assign_perm('Partner.change_partner', self.request.user, self.object)
        assign_perm('Partner.delete_partner', self.request.user, self.object)
        return resp


class PartnerDetailView(PermissionRequiredMixin, generic.DetailView):
    model = models.Partner
    permission_required = ['view_partner', ]
    pk_url_kwarg = 'id'


class PartnerUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = models.Partner
    permission_required = ['view_partner', 'change_partner']
    template_name = 'value_update.html'
    fields = '__all__'
    pk_url_kwarg = 'id'


class PartnerDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = models.Partner
    permission_required = ['view_partner', 'delete_partner']
    success_url = reverse_lazy('resource:PartnerList')


class ContractListView(PermissionListMixin, generic.ListView):
    model = models.Contract
    permission_required = ['view_contract', ]


class ContractCreateView(PermissionRequiredMixin, generic.CreateView):
    model = models.Contract
    permission_object = None
    permission_required = ['add_contract']
    template_name = "value_create.html"
    fields = '__all__'

    def form_valid(self, form):
        resp = super().form_valid(form)
        assign_perm('contract.view_contract', self.request.user, self.object)
        assign_perm('contract.change_contract', self.request.user, self.object)
        assign_perm('contract.delete_contract', self.request.user, self.object)
        return resp


class ContractDetailView(PermissionRequiredMixin, generic.DetailView):
    model = models.Contract
    permission_required = ['view_contract', ]
    pk_url_kwarg = 'id'


class ContractUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = models.Contract
    permission_required = ['view_contract', 'change_contract']
    template_name = 'value_update.html'
    fields = '__all__'
    pk_url_kwarg = 'id'


class ContractDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = models.Contract
    permission_required = ['view_contract', 'delete_contract']
    success_url = reverse_lazy('resource:ContractList')
