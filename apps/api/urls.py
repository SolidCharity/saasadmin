from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'instances', views.InstanceViewSet)

urlpatterns = [
    #path('apiadmin/', include(router.urls)),
    path('api/v1/instances/', views.InstanceApiView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
