from rest_framework import viewsets
from .serializers import *
from MyContentAnalyser.models import *


class ContentViewSet(viewsets.ModelViewSet):
   queryset = Content.objects.all()
   serializer_class = ContentSerializer

class LinksViewSet(viewsets.ModelViewSet):
   queryset = Links.objects.all()
   serializer_class = LinksSerializer

# class ContentViewSet(viewsets.ModelViewSet):
#    queryset = Content.objects.all()
#    serializer_class = ContentSerializer

# class ContentViewSet(viewsets.ModelViewSet):
#    queryset = Content.objects.all()
#    serializer_class = ContentSerializer

# class ContentViewSet(viewsets.ModelViewSet):
#    queryset = Content.objects.all()
#    serializer_class = ContentSerializer