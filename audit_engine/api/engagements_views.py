
import datetime
from django.core import serializers as dj_serializers
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView

from audit_engine.api import api_helpers
from rest_framework import serializers
from configuration import models as config_models


class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = config_models.Engagement
        fields = ['id', 'start_Date', 'end_Date', 'type', 'compliance_score', 'previous_compliance_score', 'is_active']
        read_only_fields = ['id', 'compliance_score', 'previous_compliance_score']


class AllEngagemnetSerializer(serializers.ModelSerializer):
    auditName = serializers.SerializerMethodField()
    auditStatus = serializers.SerializerMethodField()
    channelCount = serializers.SerializerMethodField()
    complienceScore = serializers.SerializerMethodField()

    class Meta:
        model = config_models.Engagement
        fields = ["auditName", "auditStatus", "channelCount", "complienceScore"]

    def get_auditName(self, engagement):
        return f'{engagement.type} Audit'

    def get_auditStatus(self, engagement):
        is_open = engagement.end_Date - datetime.datetime.now(datetime.timezone.utc)
        status =  'Open' if is_open.total_seconds() > 0 else 'Close'
        return status

    def get_channelCount(self, engagement):
        return config_models.ChannelType.objects.filter(engagement=engagement).count()


    def get_complienceScore(self, engagement):
        return engagement.compliance_score


class createEngagement(CreateAPIView):
    serializer_class = EngagementSerializer

    def create(self, request):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated

        company =  api_helpers.getUserCompany(request)
        if not company:
            raise Exception('Developer Error!!! All user should contain company')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)
        return Response(serializer.data)


@api_view(["GET"])
def getEngagementDetails(request):
    fetched, result = api_helpers.getEngagementById(request)
    if not fetched:
        return result
    serializer = EngagementSerializer(result)
    return Response(serializer.data)


@api_view(["POST"])
def deleteEngagement(request):
    fetched, result = api_helpers.getEngagementById(request)
    if not fetched:
        return result
    result.delete()
    return Response('Engagement Deleted')


@api_view(["POST"])
def editEngagement(request):
    serializer = EngagementSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    fetched, result = api_helpers.getEngagementById(request)
    if not fetched:
        return result
    new_engagement = result.update(**serializer.validated_data)
    return dj_serializers.serialize('json', new_engagement)


@api_view(['GET'])
def companyEngagements(request):
    if not request.user.is_authenticated:
        raise exceptions.NotAuthenticated
    company = api_helpers.getUserCompany(request)

    if not company:
        raise Exception('Developer Error!!! All user should contain company')

    allEngagemnets = config_models.Engagement.objects.filter(company = company)
    serializer = AllEngagemnetSerializer(allEngagemnets, many = True)
    return Response(serializer.data)


# class Engagements(RetrieveUpdateDestroyAPIView):
#     serializer_class = serializers.EngagementSerializer
#     queryset = config_model.Engagement.objects.all()

#     def get(self, request):
#         _id = request.GET.get('id')
#         if not _id:
#             return Response('Engagement Id is Required')
#         # _id = uuid.UUID(_id)
#         engagement = config_model.Engagement.objects.filter(id=_id)
#         serializer = self.serializer_class(engagement, many=True)
#         return Response(serializer.data)

#     def put(self, request):
#         if not request.user.is_authenticated:
#             raise exceptions.NotAuthenticated

#         if not request.user.company:
#             raise Exception('Developer Error!!! All user should contain company')

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(company=request.user.company)
#         return Response(serializer.data)

#     def patch(self, request):
#         self.serializer_class(data=request.data)
#         self.serializer_class.is_valid(raise_exception=True)
#         _id = request.data['id']
#         serializer = self.get_serializer(data=request.data)

#         serializer.is_valid(raise_exception=True)

#     def delete(self, request):
#         _id = request.data.get('id')
#         if not _id:
#             return Response('Engagement Id is Required')

#         _id = request.data['id']
#         x = config_model.Engagement.objects.delete(id=_id)
#         print(x)
#         return Response('Engagement Deleted')


# @api_view(["GET"])
# def getEngagementAudits(request):
#     serializer_class = serializers
#     serializer = get_serializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     serializer.save(clinc=request.user.clinic)
