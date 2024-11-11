# biosignals/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BioSignalsViewSet

# 创建 DRF 路由器，并注册 ViewSet
router = DefaultRouter()
router.register(r'biosignals', BioSignalsViewSet)

urlpatterns = [
    path('', include(router.urls)),  # 包含 DRF 路由
]
