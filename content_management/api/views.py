from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers as content_serializers
from rest_framework.generics import CreateAPIView
from content_management import models as content_models


class CreateChannelData(CreateAPIView):

    serializer_class = content_serializers.ChannelDataSerializer

    def create(self, request, channel_id):
        channel = content_models.Channel.objects.get(id=channel_id)
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
            serializer = content_serializers.CompanyDetailsSerializer(company)
        except Exception as e:
            data = {"Error": str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def post(self, request):
        channel_type = request.data["channel type"]
        channel_url = request.data["channel url"]
        channel_weightage = request.data["channel weightage"]
        return Response(request.data)
