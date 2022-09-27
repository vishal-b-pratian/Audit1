from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers as config_serializers
from configuration import models as config_models
from rest_framework.generics import CreateAPIView
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


class CreateChannel(CreateAPIView):

    serializer_class = config_serializers.ChannelSerializer

    def createChannelData(self, channel_id):

        from components.scrapper import Scrapper
        from components.preprocessor import PreProcessText, convertDataForStorage

        url_scrapper = Scrapper()
        processor = PreProcessText()
        channel = config_models.Channel.objects.get(id=channel_id)
        scraped_data = url_scrapper.scrapeURL(channel.url)
        processed_data = processor.process(scraped_data)
        scraped_data = convertDataForStorage(scraped_data)
        processed_data = convertDataForStorage(processed_data)
        instance = config_models.ChannelData.objects.create(channel=channel)
        instance.scraped_data = scraped_data
        instance.processed_data = processed_data
        instance.save()
        serializer = config_serializers.ChannelDataSerializer(instance)

        return serializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=request.user.company)
        serializer = self.createChannelData(serializer.data["id"])
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class CreateChannelData(CreateAPIView):

    serializer_class = config_serializers.ChannelDataSerializer

    def create(self, request, channel_id):
        channel = config_models.Channel.objects.get(id=channel_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(channel=channel)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class GenerateScoreCard(APIView):
    def get(self, request):

        try:
            user = request.user
            company = user.company
            serializer = config_serializers.CompanyDetailsSerializer(company)
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def post(self, request):
        channel_type = request.data["channel type"]
        channel_url = request.data["channel url"]
        channel_weightage = request.data["channel weightage"]
        return Response(request.data)
