# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from . import serializers as content_serializers
# from rest_framework.generics import CreateAPIView
# from content_management import models as content_models


# class CreateChannel(CreateAPIView):

#     serializer_class = content_serializers.ChannelSerializer

#     def __createChannelData(self, channel, scraped_data: str):

#         from content_management.components.preprocessor import (
#             PreProcessText,
#             convertDataForStorage,
#         )

#         processor = PreProcessText()
#         instance = content_models.ChannelData.objects.create(channel=channel)
#         processed_data = processor.process(scraped_data)
#         print("\n\nScarped Data: ", scraped_data, "\n\n")
#         print("\n\nProcessed Data: ", processed_data, "\n\n")
#         scraped_data = convertDataForStorage(scraped_data)
#         processed_data = convertDataForStorage(processed_data)
#         instance.scraped_data = scraped_data
#         instance.processed_data = processed_data
#         instance.save()

#     def createChannelData(self, channel_id):

#         from content_management.components.scrapper import Scrapper

#         url_scrapper = Scrapper()
#         channel = content_models.Channel.objects.get(id=channel_id)
#         scraped_data = url_scrapper.scrapeURL(channel.url)
#         for data in scraped_data:
#             self.__createChannelData(channel, data)

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(company=request.user.company)
#         self.createChannelData(serializer.data["id"])
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             serializer.data, status=status.HTTP_201_CREATED, headers=headers
#         )


# class CreateChannelData(CreateAPIView):

#     serializer_class = content_serializers.ChannelDataSerializer

#     def create(self, request, channel_id):
#         channel = content_models.Channel.objects.get(id=channel_id)
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(channel=channel)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             serializer.data, status=status.HTTP_201_CREATED, headers=headers
#         )


# class GenerateScoreCard(APIView):
#     def get(self, request):

#         try:
#             user = request.user
#             company = user.company
#             serializer = content_serializers.CompanyDetailsSerializer(company)
#         except Exception as e:
#             data = {"Error": str(e)}
#             return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data)

#     def post(self, request):
#         channel_type = request.data["channel type"]
#         channel_url = request.data["channel url"]
#         channel_weightage = request.data["channel weightage"]
#         return Response(request.data)
