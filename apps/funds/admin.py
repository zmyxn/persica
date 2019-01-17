from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CapitalFlow
from guardian.models import UserObjectPermission
from django.contrib import messages
from django.utils import timezone

# Register your models here.

from django.utils.translation import gettext_lazy as _

admin.site.disable_action('delete_selected')

def make_pass(modeladmin, request, queryset):
    for obj in queryset:
        if obj.applicant == request.user:
            messages.error(request, " %s 由您提交, 不可自审" % obj)
        elif obj.status == 1:
            messages.error(request, " %s 已通过审核, 不可变更" % obj)
        else:
            obj.status = 1
            obj.reviewer = request.user
            obj.save()
            messages.info(request, " %s 审核成功" % obj, )


def make_repay(modeladmin, request, queryset):
    for obj in queryset:
        if obj.applicant == request.user:
            messages.error(request, " %s 由您提交, 不可自偿" % obj)
        elif obj.status == 1:
            messages.error(request, " %s 已通过审核, 不可变更" % obj)
        else:
            dd = {
                "name": obj.name,
                "date": timezone.now(),
                "amount": -obj.amount,
                "currency": obj.currency,
                "type": 2,
                "company": obj.company,
                "applicant": request.user,
            }
            CapitalFlow.objects.create(**dd)
            obj.status = 1
            obj.reviewer = request.user
            obj.save()


def make_deny(modeladmin, request, queryset):
    for obj in queryset:
        if obj.status == 1:
            messages.error(request, " %s 已通过审核, 不可变更" % obj)
        else:
            obj.status = 2
            obj.reviewer = request.user
            obj.save()
            messages.info(request, " %s 设定复查成功" % obj, )


make_pass.short_description = "审核通过"
make_repay.short_description = "偿还债物"
make_deny.short_description = "要求复查"


class CapitalFlowAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'type', 'amount', 'company', 'currency', 'applicant', 'status', 'reviewer')
    readonly_fields = ('created', 'updated', 'applicant', 'status', 'reviewer')
    search_fields = ['date', 'amount', ]
    autocomplete_fields = ['company']
    actions = [make_pass, make_repay, make_deny]
    date_hierarchy = 'date'
    list_filter = ('company',)

    def save_model(self, request, obj, form, change):
        if obj.applicant is None:
            obj.applicant = request.user
        if obj.applicant != request.user:
            messages.set_level(request, messages.ERROR)
            self.message_user(request, "保存失败，仅创建者可更新信息！", messages.ERROR, )
        elif obj.status == 1:
            messages.set_level(request, messages.ERROR)
            self.message_user(request, "保存失败，已审核的记录不可修改！", messages.ERROR, )
        else:
            super().save_model(request, obj, form, change)


class Company(CapitalFlow):
    class Meta:
        proxy = True


class CompanyAdmin(CapitalFlowAdmin):
    date_hierarchy = 'date'
    list_filter = ('company',)

    def get_queryset(self, request):
        qs = super(CompanyAdmin, self).get_queryset(request)
        return qs.filter(company=1)


admin.site.register(CapitalFlow, CapitalFlowAdmin)
admin.site.register(Company, CompanyAdmin)
