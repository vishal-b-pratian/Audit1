
import datetime
from django.db.models import Q
from django.core import serializers as dj_serializers
from rest_framework import exceptions, status
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


class ChannelNameSerialzer(serializers.ModelSerializer):
    class Meta:
        model = config_models.ChannelName
        filelds = ['channel_name']


class AllChannelsSerializer(serializers.ModelSerializer):
    channelName = serializers.SerializerMethodField()

    class Meta:
        model = config_models.Channel
        fields = ['id', 'channelName']

    def get_channelName(self, channel):
        return channel.channel_name.channel_name


class AuditSerializer(serializers.ModelSerializer):
    companyId = serializers.SerializerMethodField()
    companyName = serializers.SerializerMethodField()
    auditName = serializers.SerializerMethodField()
    auditId = serializers.SerializerMethodField()
    auditStatus = serializers.SerializerMethodField()
    channels = serializers.SerializerMethodField()
    channelCount = serializers.SerializerMethodField()
    auditScore = serializers.SerializerMethodField()

    class Meta:
        model = config_models.Engagement
        fields = ["companyId", "companyName", "auditName", "auditId",
                  "auditStatus", "auditScore", "channels", "channelCount"]

    def get_companyId(self, engagement):
        return engagement.company.id

    def get_companyName(self, engagement):
        return engagement.company.name

    def get_auditName(self, engagement):
        return f'{engagement.type} Audit'

    def get_auditId(self, engagement):
        return f'{engagement.id}'

    def get_auditStatus(self, engagement):
        is_open = engagement.end_Date - datetime.datetime.now(datetime.timezone.utc)
        status = 'Open' if is_open.total_seconds() > 0 else 'Close'
        return status

    def get_channels(self, engagement):
        channels = config_models.Channel.objects.filter(engagement=engagement)
        serializer = AllChannelsSerializer(channels, many=True)
        return serializer.data

    def get_channelCount(self, engagement):
        return config_models.ChannelType.objects.filter(engagement=engagement).count()

    def get_auditScore(self, engagement):
        return engagement.compliance_score


@api_view(['GET'])
def getAllAudits(request):
    company_id = request.GET.get('CompanyId')
    if not company_id:
        return Response('Company Id not in request.', status=status.HTTP_400_BAD_REQUEST)

    company = config_models.CompanyDetails.objects.get(id=company_id)
    if not company:
        return Response('No Company instance found for the following company Id.', status=status.HTTP_400_BAD_REQUEST)

    allEngagemnets = config_models.Engagement.objects.filter(company=company)
    serializer = AuditSerializer(allEngagemnets, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def viewAuditSummary(request):
    company_id = request.GET.get('CompanyId', None)
    audit_id = request.GET.get('AuditId', None)

    if not company_id:
        return Response('Company Id not in request.', status=status.HTTP_400_BAD_REQUEST)

    if not audit_id:
        return Response('Audit Id not in request.', status=status.HTTP_400_BAD_REQUEST)

    audit = config_models.Engagement.objects.filter(Q(company__id=company_id) & Q(id=audit_id))
    if len(audit) >1:
        raise Exception('Multiple results for audit')
    audit = audit.first()
    serializer = AuditSerializer(audit)
    return Response(serializer.data)


class createEngagement(CreateAPIView):
    serializer_class = EngagementSerializer

    def create(self, request):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated

        company = api_helpers.getUserCompany(request)
        if not company:
            raise Exception('Developer Error!!! All user should contain company')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)
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

    allEngagemnets = config_models.Engagement.objects.filter(company=company)
    serializer = AllEngagemnetSerializer(allEngagemnets, many=True)
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
