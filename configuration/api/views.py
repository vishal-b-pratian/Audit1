from configuration.models import Engagement
from rest_framework.response import Response
from rest_framework.decorators import api_view
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
def getEngagementDetails(request):
    company_name = request.GET['company_name']

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

    channels = config_models.Channel.objects.all()
    serializer = config_serializers.ChannelSerializer(channels, many=True)
    return Response(serializer.data)


