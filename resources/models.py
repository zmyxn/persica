from django.db import models
from django.urls import reverse
from core.models import Tree
from guardian.models import GroupObjectPermissionBase, UserObjectPermissionBase
# Create your models here.


class Partner(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="合作商名称")
    telephone = models.CharField(max_length=30, blank=True, null=True, verbose_name="支持电话")
    website = models.CharField(max_length=30, blank=True, null=True, verbose_name="网址")
    website_background = models.CharField(max_length=30, blank=True, null=True, verbose_name="管理中心")
    website_username = models.CharField(max_length=30, blank=True, null=True, verbose_name="管理中心帐号")
    website_password = models.CharField(max_length=30, blank=True, null=True, verbose_name="管理中心密码")
    website_token = models.CharField(max_length=128, blank=True, null=True, verbose_name="管理中心token")
    website_secret = models.CharField(max_length=128, blank=True, null=True, verbose_name="管理中心secret")
    webchat = models.CharField(max_length=128, blank=True, null=True, verbose_name="联络中心")
    bank_account = models.CharField(max_length=30, blank=True, null=True, verbose_name="银行帐号")
    bank_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="帐号名称")
    bank_opening = models.CharField(max_length=30, blank=True, null=True, verbose_name="开户银行")
    alipay_auth_info = models.CharField(max_length=30, blank=True, null=True, verbose_name="支付宝识别信息")
    alipay_account = models.CharField(max_length=30, blank=True, null=True, verbose_name="支付宝帐号名")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_partner', 'Can view partner'),
            ('view_partner_confidential', 'Can view partner confidential'),
            ('view_partner_confidentiality', 'Can view partner confidentiality'),
        )
        verbose_name = "供应商"

    def get_absolute_url(self):
        return reverse('resource:PartnerDetail', args=[self.id])


class People(models.Model):
    partner = models.ForeignKey(Partner, on_delete=False, blank=True, null=True, verbose_name="合作商")
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name="联系人")
    qq = models.CharField(max_length=128, blank=True, null=True, verbose_name="QQ")
    telephone = models.CharField(max_length=128, blank=True, null=True, verbose_name="Telephone")
    email = models.CharField(max_length=128, blank=True, null=True, verbose_name="Email")
    wechat = models.CharField(max_length=128, blank=True, null=True, verbose_name="Wechat")
    skype = models.CharField(max_length=128, blank=True, null=True, verbose_name="Skype")
    whatsapp = models.CharField(max_length=128, blank=True, null=True, verbose_name="Whatsapp")
    telegram = models.CharField(max_length=128, blank=True, null=True, verbose_name="Telegram")


class PartnerUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Partner, on_delete=models.CASCADE)


class PartnerGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Partner, on_delete=models.CASCADE)


class Contract(models.Model):
    sn = models.CharField(max_length=128, unique=True, verbose_name="合同编号")
    name = models.CharField(max_length=64, verbose_name="合同名称")
    price = models.IntegerField(verbose_name="合同金额")
    detail = models.TextField(blank=True, null=True, verbose_name="合同详细")
    start_day = models.DateField(blank=True, null=True, verbose_name="生效日期")
    end_day = models.DateField(blank=True, null=True, verbose_name="失效日期")
    create_date = models.DateField(auto_now_add=True, verbose_name="记录创建日期")
    update_date = models.DateField(auto_now=True, verbose_name="记录更新日期")
    memo = models.TextField(blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_contract', 'Can view contract'),
        )
        verbose_name = "合同"

    def get_absolute_url(self):
        return reverse('resource:ContractDetail', args=[self.id])


class ContractUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Contract, on_delete=models.CASCADE)


class ContractGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Contract, on_delete=models.CASCADE)


class Location(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="机房名称")
    contract = models.ForeignKey(Contract, on_delete=False, blank=True, null=True, verbose_name="关联合同")
    memo = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机房"


class Resource(models.Model):
    __status__ = (
        (0, '在线'),
        (1, '离线'),
        (2, '备用'),
        (3, '故障'),
        (4, '待审'),
    )
    __type__ = (
        (0, '采购'),
        (1, '租借'),
        (2, '置换'),
        (3, '自制')
    )

    resource_type = models.ForeignKey(Tree, on_delete=False, related_name='resource_type', verbose_name="资源类型")
    name = models.CharField(max_length=64, unique=True, verbose_name="资源名称")
    sn = models.CharField(max_length=128, unique=True, verbose_name="设备sn")
    status = models.SmallIntegerField(choices=__status__, default=4, verbose_name="设备状态")
    create_date = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="记录创建时间")
    update_date = models.DateField(auto_now=True, null=True, blank=True, verbose_name="记录更新时间")
    contract = models.ForeignKey(Contract, on_delete=False, blank=True, null=True, verbose_name="关联合同")
    group = models.ForeignKey(Tree, on_delete=False, related_name='resource_platform', null=True, blank=True, verbose_name="归属组织")
    # approved_by = models.ForeignKey(User, null=True, blank=True, related_name="approved_device", verbose_name="审核人")
    # start_day = models.DateField(blank=True, null=True, verbose_name="生效日期")
    end_day = models.DateField(blank=True, null=True, verbose_name="过期/过保日期")
    # admin_by = models.ForeignKey(User, null=True, blank=True, related_name="manage_device", verbose_name="管理员")
    supplier_by = models.ForeignKey(Partner, on_delete=False, null=True, blank=True, verbose_name="关联供应商")
    idcs = models.ForeignKey(Location, on_delete=False, null=True, blank=True, verbose_name="关联IDC")
    acquirementway = models.SmallIntegerField(choices=__type__, default=0, verbose_name="获得方式")

    def __str__(self):
        return self.name

    class Meta:
        default_permissions = ('add', 'change', 'delete')
        permissions = (
            ('view_resource', 'Can view Resource'),
        )
        verbose_name = "资源总表"
        ordering = ['-create_date']

    def get_absolute_url(self):
        return reverse('resource:ResourceDetail', args=[self.id])

    def basic_to_ansible(self):
        "manage_ip"
        "username"
        "password"
        "manage_port"
        "ssh_key"
        "command_name"
        "command_args"


class ResourceUserObjectPermission(UserObjectPermissionBase):
    content_object = models.ForeignKey(Resource, on_delete=models.CASCADE)


class ResourceGroupObjectPermission(GroupObjectPermissionBase):
    content_object = models.ForeignKey(Resource, on_delete=models.CASCADE)


class Cabinet(models.Model):
    __type__ = (
        (0, '24U'),
        (1, '36U'),
        (2, '42U'),
    )
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    power = models.CharField(max_length=64, blank=True, null=True, verbose_name="电力")
    type = models.SmallIntegerField(choices=__type__, default="2", verbose_name="机柜高度")


class Racklayout(models.Model):
    resource = models.ForeignKey(Resource, on_delete=False)
    position = models.SmallIntegerField(verbose_name="设备位置,底为1")
    resource_name = models.ForeignKey(Resource, on_delete=False, related_name="connect_resource", verbose_name="关联上架设备")

    class Meta:
        verbose_name = "机柜布局"


class ServerDevice(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    host = models.ForeignKey('self', on_delete=False, related_name="host_server", blank=True, null=True, verbose_name="宿主机")
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name="服务器型号")
    os_type = models.CharField(max_length=64, blank=True, null=True, verbose_name="操作系统类型")
    os_release = models.CharField(max_length=64, blank=True, null=True, verbose_name="操作系统版本")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name="SN号")
    cpu_model = models.CharField(verbose_name="CPU型号", default=1, max_length=64)
    cpu_manufacturer = models.CharField(max_length=64, default=1, blank=True, null=True, verbose_name="CPU制造厂商")
    cpu_core = models.CharField(verbose_name="CPU核数", default=1, max_length=32)
    cpu_processor = models.CharField(verbose_name="CPU进程数", default=1, max_length=32)
    cpu_quantity = models.CharField(verbose_name="CPU数量", default=1, max_length=32)
    ram_total = models.CharField(verbose_name="整机内存容量", default=1, max_length=32)
    disk_total = models.CharField(verbose_name="整机磁盘容量", default=1, max_length=32)

    def __str__(self):
        return str(self.resource.sn)

    class Meta:
        verbose_name = "服务器列表"

    def get_absolute_url(self):
        return reverse('resource:ResourceDetail', args=[self.resource])


class NetworkDevice(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name="型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="固件版本")
    device_detail = models.TextField(blank=True, null=True, verbose_name="详细配置")
    forwarding_rate = models.TextField(blank=True, null=True, verbose_name="转发速率")
    backboard_bandwidth = models.TextField(blank=True, null=True, verbose_name="背板带宽")

    class Meta:
        verbose_name = "网络设备"


class StorageDevice(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name="型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="固件版本")

    class Meta:
        verbose_name = "存储设备"


class SecurityDevice(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(max_length=128, blank=True, null=True, verbose_name="型号")
    firmware = models.CharField(max_length=128, blank=True, null=True, verbose_name="固件版本")
    device_detail = models.TextField(blank=True, null=True, verbose_name="详细配置")

    class Meta:
        verbose_name = "安全设备"


class Software(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="软件名称")
    device_detail = models.TextField(blank=True, null=True, verbose_name="详细配置")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "软件"


class VirtualDevice(models.Model):
    pass

    class Meta:
        verbose_name = "虚拟设备"


class CPU(models.Model):
    resource = models.ForeignKey(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(verbose_name="型号", max_length=64)
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name="制造厂商")
    core = models.CharField(verbose_name="核数", max_length=32)
    processor = models.CharField(verbose_name="进程数", max_length=32)

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "CPU详情"


class RAM(models.Model):
    resource = models.ForeignKey(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(verbose_name="型号", max_length=32)
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name="制造厂商")
    slot = models.CharField(max_length=64, verbose_name="插槽位置")
    capacity = models.CharField(max_length=64, blank=True, null=True, verbose_name="容量大小")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name="硬件SN号")

    class Meta:
        verbose_name = "内存详情"
        unique_together = ('resource', 'slot')


class Disk(models.Model):
    __choice__ = (
        ('STAT', 'STAT'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
        ('unknown', 'unknown'),
    )
    resource = models.ForeignKey(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(verbose_name="型号", max_length=128)
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name="制造厂商")
    slot = models.CharField(max_length=64, verbose_name="插槽位置")
    capacity = models.CharField(max_length=64, blank=True, null=True, verbose_name="容量大小")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name="硬件SN号")
    interface = models.CharField(choices=__choice__, default="unknown", max_length=16)

    class Meta:
        verbose_name = "磁盘详情"
        unique_together = ('resource', 'sn')


class NIC(models.Model):
    resource = models.ForeignKey(Resource, on_delete=False, verbose_name="关联资源")
    model = models.CharField(verbose_name="型号", max_length=128)
    manufacturer = models.CharField(max_length=64, blank=True, null=True, verbose_name="制造厂商")
    slot = models.CharField(max_length=64, verbose_name="插槽位置")
    sn = models.CharField(max_length=128, blank=True, null=True, verbose_name="硬件SN号")
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="网卡名称")
    mac = models.CharField(max_length=64, verbose_name="MAC地址")
    bonding = models.CharField(max_length=64, blank=True, null=True, verbose_name="绑定地址")
    connect = models.ForeignKey(Resource, on_delete=False, blank=True, null=True, related_name='connect_device')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "网卡详情"
        unique_together = ('resource', 'model', 'mac')


class IP(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    mask = models.GenericIPAddressField(verbose_name="子网掩码")
    use = models.ForeignKey(Tree, on_delete=False, verbose_name="作用")

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = "IP列表"


class InAndOutDevice(models.Model):
    pass


class TerminalEquipment(models.Model):
    pass


class Certificat(models.Model):
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="证书名称")
    detail = models.CharField(max_length=128, verbose_name="证书内容")
    end_day = models.DateField(blank=True, null=True, verbose_name="失效日期")
    url = models.CharField(max_length=128, verbose_name="存放位置")
    station = models.ForeignKey(Tree, on_delete=False, related_name="station_tree", verbose_name="归属站点")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "证书存放"


class Domain(models.Model):
    __status__ = (
        (0, 'True'),
        (1, 'False'),
    )
    resource = models.OneToOneField(Resource, on_delete=False, verbose_name="关联资源")
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="名称")
    domain_id = models.CharField(max_length=64, blank=True, null=True, verbose_name="domain_id")
    registrar = models.ForeignKey(Partner, on_delete=False, related_name="registrar_supplier", verbose_name="注册商")
    dnssupplier = models.ForeignKey(Partner, on_delete=False, related_name="dns_supplier", blank=True, null=True, verbose_name="解析商")
    created_time = models.DateField(null=True, blank=True, verbose_name="注册时间")
    expires_time = models.DateField(null=True, blank=True, verbose_name="到期时间")
    privacy = models.SmallIntegerField(choices=__status__, blank=True, null=True, verbose_name="隐私保护")
    certificat = models.ForeignKey(Certificat, on_delete=False, blank=True, null=True, verbose_name="关联证书")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "IP列表"


class Dns(models.Model):
    resource = models.ForeignKey(Resource, on_delete=False, verbose_name="关联资源")
    record_id = models.CharField(max_length=128, blank=True, null=True, verbose_name="记录ID")
    name = models.CharField(max_length=64, blank=True, null=True, verbose_name="sub_domain")
    type = models.CharField(max_length=64, blank=True, null=True, verbose_name="record_type")
    ttl = models.CharField(max_length=64, blank=True, null=True, verbose_name="record_ttl")
    value = models.CharField(max_length=64, blank=True, null=True, verbose_name="record_value")
    line_id = models.CharField(max_length=64, blank=True, null=True, verbose_name="record_line_id")
    mx = models.CharField(max_length=64, blank=True, null=True, verbose_name="record_mx")


class EventLog(models.Model):
    __choice__ = (
        (0, '配件变更'),
        (1, '设备下线'),
        (2, '设备上线'),
        (3, '设备维护'),
        (4, '业务上线'),
        (5, '其他'),
        (6, '新增资源'),
    )
    name = models.CharField(max_length=128, verbose_name="事件名称")
    resource = models.ForeignKey(Resource, blank=True, null=True, on_delete=models.SET_NULL)
    event_type = models.SmallIntegerField(choices=__choice__, default=4, verbose_name="事件类型")
    detail = models.TextField(verbose_name="详情")
    date = models.DateField(auto_now_add=True, verbose_name="事件时间")
    # user = models.ForeignKey(User, related_name="executive_user", blank=True, null=True, verbose_name="执行人", on_delete=models.SET_NULL)
    memo = models.TextField(blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name = "事件记录"


class EnvAndResource(models.Model):
    pass
