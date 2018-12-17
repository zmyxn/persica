from django.conf.urls import url
from . import views

app_name = "resources"
urlpatterns = [
    # Resource Model
    url('^resource/list/$', views.ResourceListView.as_view(), name='ResourceList'),
    url('^resource/Classification/(?P<id>\d+)$', views.ResourceListView.as_view(), name='ResourceClassification'),
    url('^resource/create/$', views.ResourceCreateView.as_view(), name='ResourceCreateIndex'),
    url('^resource/create/(?P<id>\d+)$', views.ResourceCreateView.as_view(), name='ResourceCreate'),
    url('^resource/delete/(?P<id>\d+)$', views.ResourceDeleteView.as_view(), name='ResourceDelete'),
    url('^resource/detail/(?P<id>\d+)$', views.ResourceDetailView.as_view(), name='ResourceDetail'),
    url('^resource/update/(?P<id>\d+)$', views.ResourceUpdateView.as_view(), name='ResourceUpdate'),
    url('^resource/(?P<ff>\w+)/(?P<id>\d+)$', views.ResourceDetailView.as_view(), name='ResourceCollect'),
    # Partner Model
    url('^partner/list/$', views.PartnerListView.as_view(), name='PartnerList'),
    url('^partner/create/$', views.PartnerCreateView.as_view(), name='PartnerCreate'),
    url('^partner/delete/(?P<id>\d+)$', views.PartnerDeleteView.as_view(), name='PartnerDelete'),
    url('^partner/detail/(?P<id>\d+)$', views.PartnerDetailView.as_view(), name='PartnerDetail'),
    url('^partner/update/(?P<id>\d+)$', views.PartnerUpdateView.as_view(), name='PartnerUpdate'),
    # Contract Model
    url('^contract/list/$', views.ContractListView.as_view(), name='ContractList'),
    url('^contract/create/$', views.ContractCreateView.as_view(), name='ContractCreate'),
    url('^contract/delete/(?P<id>\d+)$', views.ContractDeleteView.as_view(), name='ContractDelete'),
    url('^contract/detail/(?P<id>\d+)$', views.ContractDetailView.as_view(), name='ContractDetail'),
    url('^contract/update/(?P<id>\d+)$', views.ContractUpdateView.as_view(), name='ContractUpdate'),
]
