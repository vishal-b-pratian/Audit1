from configuration.models import Engagement
from django.core import serializers
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import dateutil.parser as dateTimeparser
from itertools import chain
from . import serializers as config_serializers
from configuration import models as config_models
from django.contrib.auth import models as auth_models


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET", "/api/users/"},
        {"GET", "/api/users/<int:id>/"},
        {"GET", "/api/company-details/"},
        {"GET", "/api/company-details/<uuid:id>/"},
        {"GET / POST", "/api/create-channel/"},
        {"GET / POST", "/api/create-channel-data/"},
        {"GET", "/api/engagement-details/"}
    ]

    return Response(routes)


@api_view(["GET"])
def getUsersData(request):

    users = auth_models.User.objects.all()
    serializer = config_serializers.UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getCompanyDetailsData(request):

    company_details = config_models.CompanyDetails.objects.all()
    serializer = config_serializers.CompanyDetailsSerializer(company_details, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getEngagementDetails(request,company_name):

    company_details = config_models.CompanyDetails.objects.get(name = company_name)
    engagement_details = config_models.Engagement.objects.filter(company = company_details)
    serializer = config_serializers.EngagementDetailsSerializer(engagement_details, many=True)
    print(serializer.data)
    return Response(serializer.data)



@api_view(["GET"])
def getUrlDetailsChannelType(request,company_name, engagement_type, channel_type):
  
    company_details = config_models.CompanyDetails.objects.get(name = company_name)
    channel_type_object = config_models.ChannelType.objects.get(channel_type= channel_type)
    engagement_details = config_models.Engagement.objects.filter(company = company_details,type = engagement_type)
    for engagement in engagement_details:
        url_details = config_models.Channel.objects.filter(engagement = engagement, type_name = channel_type_object)
    serializer = config_serializers.UrlDetailsChannelTypeSerializer(url_details, many=True)
    print(serializer.data)
    return Response(serializer.data)
  

@api_view(["GET"])
def getUrlDetailsChannel(request,company_name, engagement_type, channel_name):

    channel_name_object = config_models.ChannelName.objects.get(channel_name= channel_name)
    company_details = config_models.CompanyDetails.objects.get(name = company_name)
    
    engagement_details = config_models.Engagement.objects.filter(company = company_details,type = engagement_type)
    for engagement in engagement_details:
        url_details = config_models.Channel.objects.filter(engagement = engagement, channel_name = channel_name_object)
    serializer = config_serializers.UrlDetailsChannelSerializer(url_details, many=True)
    print(serializer.data)
    return Response(serializer.data)

@api_view(["GET"])
def getChannelsData(request,company_name):
    company_details = config_models.CompanyDetails.objects.get(name = company_name)
    engagement_details = config_models.Engagement.objects.filter(company = company_details)
    channels = []
    for engagement in engagement_details:
        if engagement.is_active:
            channels.append(config_models.Channel.objects.filter(engagement = engagement)) 
    serializer_data = []
    for channel in channels:
       
        serializer_data.append(config_serializers.ChannelSerializer(channel, many=True).data) 
                 
    return Response(serializer_data)

@api_view(["POST"])
def addEngagement(request):
    # Engagement = request.data.get('engagement')
    serializer = config_serializers.EngagementSerializer(data = request.data.get('engagement'))
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.validated_data)

    # print(Engagement)
    # end_date = dateTimeparser.parse(Engagement.get('end_Date'))
    # type = Engagement['type']
    # company_details = config_models.CompanyDetails.objects.get(name = Engagement.get('company'))
    # # print(Engagement)
    # engagement = config_models.Engagement.objects.create(company = company_details,type = type, end_Date = end_date)
    # x = {}
    # x['company'] = engagement.company.id
    # x['start_Date'] = engagement.start_Date
    # return Response(x)
    
# def addChannel(request):
#     if request.method == "GET":

#     else:
#         serializer = config_serializers.ChannelSerializer(data = request.data.get('channel'))
#         serializer .is_valid(raise_exception = True)
#         serializer.save()
#         return Response(serializer.validated_data)

