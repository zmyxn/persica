from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from apps.common.models import Tree
from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase
# Create your models here.


class CapitalFlow(models.Model):
    __type__ = (
        (0, '注资'),
        (1, '垫付'),
        (2, '偿还'),
        (3, '借出'),
        (4, '分红'),
        (5, '工资'),
        (6, '盈利'),
    )
    __currency__ = (
        (0, 'PHP'),
        (1, 'CNY'),
    )
    __status__ = (
        (0, '待审'),
        (1, '通过'),
        (2, '复查'),
    )
    name = models.CharField(max_length=128, verbose_name="标题")
    date = models.DateField(max_length=30, blank=True, null=True, verbose_name="交易时间")
    amount = models.FloatField(verbose_name="金额")
    currency = models.SmallIntegerField(choices=__currency__, default=0, verbose_name="货币类别")
    created = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="记录创建时间")
    updated = models.DateField(auto_now=True, null=True, blank=True, verbose_name="记录更新时间")
    type = models.SmallIntegerField(choices=__type__,default=0, verbose_name="记录类别")
    company = models.ForeignKey(Tree, on_delete=False, blank=True, null=True, verbose_name="归属公司")
    applicant = models.ForeignKey(User, on_delete=False, blank=True, null=True, related_name="applicant_user", verbose_name="提交人")
    reviewer = models.ForeignKey(User, on_delete=False, blank=True, null=True, related_name="reviewer_user", verbose_name="审核人")
    status  = models.SmallIntegerField(choices=__status__, default=0, verbose_name="状态")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_partner', 'Can view CapitalFlow'),
        )
        verbose_name = "资金流水"

    def get_absolute_url(self):
        return reverse('resource:PartnerDetail', args=[self.id])


