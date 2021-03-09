from django.urls import include, path
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'instances', views.SaaSInstanceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
#    path('apiadmin/', include(router.urls)),
    path('apiadmin/', views.SaaSInstanceApiView.as_view()),
    path('apiadmin/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
