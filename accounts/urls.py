from django.conf.urls import url
from . import views

app_name = "accounts"
urlpatterns = [
    # Login & Logout
    url('^login/', views.LoginView.as_view(), name='login'),
    url('^logout/$', views.LogoutView.as_view(), name='logout'),
    # User Model
    url('^user/list/$', views.UserListView.as_view(), name='UserList'),
    url('^user/create/$', views.UserCreateView.as_view(), name='UserCreate'),
    url('^user/detail/(?P<id>\d+)$', views.UserDetailView.as_view(), name='UserDetail'),
    url('^user/update/(?P<id>\d+)$', views.UserUpdateView.as_view(), name='UserUpdate'),
    # # Role Model
    # url('^role/list/$', views.RoleListView.as_view(), name='RoleList'),
    # url('^role/create/$', views.RoleCreateView.as_view(), name='RoleCreate'),
    # url('^role/delete/(?P<id>\d+)$', views.RoleDeleteView.as_view(), name='RoleDel'),
    # url('^role/detail/(?P<id>\d+)$', views.RoleDetailView.as_view(), name='RoleDetail'),
    # url('^role/update/(?P<id>\d+)$', views.RoleUpdateView.as_view(), name='RoleUpdate'),
    # # # Permission Model
    # url('^permission/list/$', views.PermissionListView.as_view(), name='PermissionList'),
    # url('^permission/create/$', views.PermissionCreateView.as_view(), name='PermissionCreate'),
    # url('^permission/delete/(?P<id>\d+)$', views.PermissionDeleteView.as_view(), name='PermissionDel'),
    # url('^permission/detail/(?P<id>\d+)$', views.PermissionDetailView.as_view(), name='PermissionDetail'),
    # url('^permission/update/(?P<id>\d+)$', views.PermissionUpdateView.as_view(), name='PermissionUpdate'),
    # url('^permission/deny/(?P<id>\d+)$', views.PermissionDetailView.as_view(), name='PermissionDeny'),
]