from django import forms

from django.forms import ModelForm
from .models import Resource, ServerDevice, NetworkDevice, StorageDevice, SecurityDevice
from .models import CPU, RAM, Disk, NIC
from .models import Location, IP, Cabinet, Software
from .models import Certificat, Domain


class ResourceForm(ModelForm):
    class Meta:
        model = Resource
        fields = '__all__'
        exclude = {'status', 'start_day'}


class ServerDeviceForm(ModelForm):
    class Meta:
        model = ServerDevice
        fields = '__all__'
        exclude = {'resource'}


class NetworkDeviceForm(ModelForm):
    class Meta:
        model = NetworkDevice
        fields = '__all__'
        exclude = {'resource'}


class StorageDeviceForm(ModelForm):
    class Meta:
        model = StorageDevice
        fields = '__all__'
        exclude = {'resource'}


class SecurityDeviceForm(ModelForm):
    class Meta:
        model = SecurityDevice
        fields = '__all__'
        exclude = {'resource'}


class IDCForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class IPForm(ModelForm):
    class Meta:
        model = IP
        fields = '__all__'


class CabinetForm(ModelForm):
    class Meta:
        model = Cabinet
        fields = '__all__'


class SoftwareForm(ModelForm):
    class Meta:
        model = Software
        fields = '__all__'


class CPUForm(ModelForm):
    class Meta:
        model = CPU
        exclude = {'id'}


class RAMForm(ModelForm):
    class Meta:
        model = RAM
        exclude = {"id"}


class DiskForm(ModelForm):
    class Meta:
        model = Disk
        exclude = {"id"}


class NICForm(ModelForm):
    class Meta:
        model = NIC
        exclude = {"id"}


class CertificatForm(ModelForm):
    class Meta:
        model = Certificat
        fields = '__all__'
        exclude = {'resource'}


class DomainForm(ModelForm):
    class Meta:
        model = Domain
        fields = '__all__'
        exclude = {'resource'}


class TerminalEquipmentForm(ModelForm):
    pass


class InAndOutDevicesForm(ModelForm):
    pass
