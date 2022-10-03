from re import M
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from content_management.models import *
from configuration.models import Channel
import json

from content_management.components.scrapper import Scrapper
from content_management.components.content_analyser import ContentAnalyser

@api_view(['GET', 'POST'])
def LinksViewSet(request):
   if request.method == 'POST':
      links = Links.objects.all()
      channel_id = request.data.get('channel_id', None)
      if not channel_id:
         return Response('Channel ID not sent', status=status.HTTP_400_BAD_REQUEST)
      serializer = LinksSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      validated_data = serializer.validated_data
      channel_obj =  Channel.objects.filter(id=channel_id).first()
      validated_data['channel'] = channel_obj

      link_obj = Links.objects.create(**validated_data)
      url = validated_data['url']
      link = Links.objects.get(channel_id=channel_id)
      try:
      # parameters = json.load(link.parameters)
         parameters = eval(serializer.data['parameters'])
         scraper = Scrapper()
         scrape_data = scraper.scrapeURL(url)[0]

         content = Content.objects.create(link=link, main_content=scrape_data)

         contents = ContentAnalyser(scrape_data, parameters)

         processed_words = contents.preprocessing()
         content_info = ContentFetchInfo.objects.create(content=content, processed_words=processed_words)

         mapped_keywords = contents.audit_frequency()
         mapped_keywords_count = contents.count_mapped_keywords()
         MappedKeyWords.objects.create(content_info=content_info,
                                       mapped_keywords=mapped_keywords, mapped_keywords_count=mapped_keywords_count)

         unmapped_keywords = contents.final_unmapped()
         unmapped_keywords_count = len(unmapped_keywords)
         UnmappedKeywords.objects.create(
               content_info=content_info, unmapped_keywords=unmapped_keywords, unmapped_keywords_count=unmapped_keywords_count)

         return Response("Fetch Complete", status=status.HTTP_201_CREATED)
      except:
         link_obj.delete()
         return Response("Internal Logic error", status=status.HTTP_501_NOT_IMPLEMENTED)
   if request.method == 'GET':
         links = Links.objects.all()
         serializer = LinksSerializer(links, many=True)
         return Response(serializer.data)


@api_view(['GET'])
def View_Keyword_Summary(request,channel_id):
    if request.method == 'GET':
      contentfetchmapped = MappedKeyWords.objects.all()
      contentfetchUnmapped = UnmappedKeywords.objects.all()
        
      if channel_id is not None:
         contentfetchmapped = contentfetchmapped.filter(content_info__content__link__channel_id__icontains=channel_id)
         contentfetchUnmapped = contentfetchUnmapped.filter(content_info__content__link__channel_id__icontains=channel_id)

      contentfetch_mapped_serializer = ContentFetchMappedSerializer(contentfetchmapped, many=True)
      contentfetch_unmapped_serializer = ContentFetchUnmappedSerializer(contentfetchUnmapped, many=True)
      
      try:
         map_count = contentfetch_mapped_serializer.data[0]['mapped_keywords_count']
         unmap_count = contentfetch_unmapped_serializer.data[0]['unmapped_keywords_count']
         total_count = map_count + unmap_count
         
         Count_dict = dict()
         Count_dict['total_words_count'] = total_count
         Count_dict['mapped_keywords_count'] = map_count
         Count_dict['unmapped_keywords_count'] = unmap_count
         
         return Response(Count_dict)
      except:
         return Response("Not found",status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Content_Fetch_Unmapped(request,channel_id):
    if request.method == 'GET':
        contentfetch = UnmappedKeywords.objects.all()
        if channel_id is not None:
            contentfetch = contentfetch.filter(content_info__content__link__channel_id__icontains=channel_id)
        try:
            contentfetch_serializer = ContentFetchUnmappedSerializer(contentfetch, many=True)
            list_unmapped = contentfetch_serializer.data[0]['unmapped_keywords']
            return Response(eval(list_unmapped))
        except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Content_Fetch_Mapped(request,channel_id):
    if request.method == 'GET':
        contentfetchmapped = MappedKeyWords.objects.all()
        if channel_id is not None:
            contentfetchmapped = contentfetchmapped.filter(content_info__content__link__channel_id__icontains=channel_id)
        contentfetch_mapped_serializer = ContentFetchMappedSerializer(contentfetchmapped, many=True)
        try:
            mapped_keywords = contentfetch_mapped_serializer.data[0]['mapped_keywords']
            mapped_keywords = eval(mapped_keywords)
            return Response(mapped_keywords)
        except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

# Returns Proccessed Word response as list
# Use url viewContentSummary/<channel_id>
@api_view(['GET'])
def View_Content_Summary(request,channel_id):
    if request.method == 'GET':
        contentfetch = ContentFetchInfo.objects.all()
        if channel_id is not None:
            contentfetch = contentfetch.filter(content__link__channel_id__icontains=channel_id)
        try:
            contentfetch_serializer = ContentFetchInfoSerializer(contentfetch, many=True)
            content_summary = contentfetch_serializer.data[0]['processed_words']
            return Response(eval(content_summary))
        except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

# Returns Original Content response as string
# Use url viewOriginalContent/<channel_id>
@api_view(['GET'])
def View_Original_Content(request,channel_id):
    if request.method == 'GET':
        contentfetch = Content.objects.all()
        if channel_id is not None:
            contentfetch = contentfetch.filter(link__channel_id__icontains=channel_id)
        try:
            contentfetch_serializer = ContentSerializer(contentfetch, many=True)
            original_content = contentfetch_serializer.data[0]['main_content']
            print(type(original_content))
            return Response(original_content)
        except:
            return Response("Not Found")

@api_view(['GET'])
def Content_Fetch_DateTime(request,channel_id):
    if request.method == 'GET':
        contentfetch = ContentFetchInfo.objects.all()
        if channel_id is not None:
            contentfetch = contentfetch.filter(content__link__channel_id__icontains=channel_id)
        try:
            contentfetch_DateTime_serializer = ContentFetchInfoSerializer(contentfetch, many=True)
            list_DateTime = contentfetch_DateTime_serializer.data[0]['created']
            Date = list_DateTime[0:10]
            Time = list_DateTime[11:19]
            response = {}
            response['Date'] = Date
            response['Time'] = Time
            return Response(response)
        except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def Fetch_Parameters(request,channel_id):
      if request.method == "GET":
         parameters_fetch = Links.objects.all()
         if channel_id is not None:
            parameters_fetch = parameters_fetch.filter(channel_id=channel_id)
         try:
            parameter_fetch_serializer = LinksSerializer(parameters_fetch, many=True)
            Parameters_list = parameter_fetch_serializer.data[0]['parameters']
            return Response((eval(Parameters_list)).keys())
         except:
            return Response("Not Found",status=status.HTTP_404_NOT_FOUND)