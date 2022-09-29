from rest_framework import serializers
from MyContentAnalyser.models import *

class LinksSerializer(serializers.ModelSerializer):
    class Meta:
       model = Links
       fields = ('channel_id','url')

class ContentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Content
       fields = ('channel_id','title','main_content')

# class ContentSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Content
#        fields = ()


# class ContentSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Content
#        fields = ()

# class ContentSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Content
#        fields = ()

