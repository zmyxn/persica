from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.
class Structure(models.Model):
    """
    组织架构
    """
    type_choices = (("unit", "单位"), ("department", "部门"))
    name = models.CharField(max_length=60, verbose_name="名称")
    type = models.CharField(max_length=20, choices=type_choices, default="department", verbose_name="类型")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父类架构")

    class Meta:
        verbose_name = "组织架构"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    __status__ = (
        (0, '未申请'),
        (1, '首次申请'),
        (2, '首次办理中'),
        (3, '首办已完成'),
        (1, '续签申请'),
        (2, '续签办理中'),
        (3, '续签已完成'),
    )
    __choice__ = (
        (0, '直飞'),
        (1, '转机'),
    )
    __skill_level__ = (
        (0, '初级'),
        (1, '中级'),
        (2, '高级'),
    )
    __residence_levels__ = (
        (0, '一级'),
        (1, '二级'),
        (1, '三级'),
    )

    ldap_name = models.CharField(max_length=64, blank=True, verbose_name="LDAP帐号")
    entry_date = models.DateField(null=True, blank=True,verbose_name="入职时间")
    official_date = models.DateField(null=True, blank=True,verbose_name="转正时间")
    resign_date = models.DateField(null=True, blank=True,verbose_name="离职时间")
    skill_level = models.SmallIntegerField(choices=__skill_level__, default=0, verbose_name="技能等级")
    air_levels = models.SmallIntegerField(choices=__choice__, default=0, verbose_name="机票报销类别")
    residence_levels = models.SmallIntegerField(choices=__residence_levels__, default=0, verbose_name="住宿报销类别")
    rfid = models.CharField(null=True, blank=True, max_length=64, verbose_name="大楼ID")
    rfid_name = models.CharField(null=True, blank=True, max_length=64, verbose_name="大楼ID名称")
    work_phone = models.BigIntegerField(null=True, blank=True, verbose_name="工作手机号码")
    position = models.ForeignKey(Structure, on_delete=False, null=True, blank=True, related_name="position_tree", verbose_name="职务")
    department = models.ForeignKey(Structure, on_delete=False, null=True, blank=True, related_name="department_tree", verbose_name="组织部门")
    visa_status = models.SmallIntegerField(choices=__status__, default=0, verbose_name="工签状态")
    visa_issue_date = models.DateField(null=True, blank=True,verbose_name="工签申请时间")
    visa_expir_date = models.DateField(null=True, blank=True, verbose_name="工签过期时间")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('accounts:UserDetail', args=[self.id])