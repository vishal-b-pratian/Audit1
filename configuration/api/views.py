from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers as config_serializers
from configuration import models as config_models
from django.contrib.auth import models as auth_models
from content_management import models as content_models

from rest_framework.generics import CreateAPIView

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

    def __createChannelData(self, channel, scraped_data: str):

        from content_management.components.preprocessor import (
            PreProcessText,
            convertDataForStorage,
        )

        processor = PreProcessText()
        instance = content_models.ChannelData.objects.create(channel=channel)
        processed_data = processor.process(scraped_data)
        print("\n\nScarped Data: ", scraped_data, "\n\n")
        print("\n\nProcessed Data: ", processed_data, "\n\n")
        scraped_data = convertDataForStorage(scraped_data)
        processed_data = convertDataForStorage(processed_data)
        instance.scraped_data = scraped_data
        instance.processed_data = processed_data
        instance.save()

    def createChannelData(self, channel_id):

        from content_management.components.scrapper import Scrapper

        url_scrapper = Scrapper()
        channel = content_models.Channel.objects.get(id=channel_id)
        scraped_data = url_scrapper.scrapeURL(channel.url)
        for data in scraped_data:
            self.__createChannelData(channel, data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=request.user.company)
        self.createChannelData(serializer.data["id"])
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

