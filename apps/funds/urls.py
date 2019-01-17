from django.conf.urls import url,include
from rest_framework import routers
from . import views


app_name = "apps.common"

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
# router.register(r'tree', api_views.TreeViewSet)


urlpatterns = [

]

urlpatterns += router.urls
