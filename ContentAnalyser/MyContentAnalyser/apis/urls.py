from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'content', ContentViewSet)
router.register(r'link', LinksViewSet)

urlpatterns = [
   path('', include(router.urls)),
] 
    
# urlpatterns = [
#         path('', views.index)
# ]  