from symbol import parameters
from rest_framework import serializers
from content_management.models import *

class LinksSerializer(serializers.ModelSerializer):
    class Meta:
       model = Links
       fields = ('channel_id','url','parameters',"title")

class ContentFetchMappedSerializer(serializers.ModelSerializer):
    class Meta:
        model = MappedKeyWords
        fields = ('content_info','mapped_keywords','mapped_keywords_count','created','updated')

class ContentFetchUnmappedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnmappedKeywords
        fields = ('content_info','unmapped_keywords','unmapped_keywords_count','created','updated')

class ContentFetchInfoSerializer(serializers.ModelSerializer):
   class Meta:
       model = ContentFetchInfo
       fields = ('content','processed_words','created','updated')

class ContentSerializer(serializers.ModelSerializer):
   class Meta:
       model = Content
       fields = ('link','main_content')
