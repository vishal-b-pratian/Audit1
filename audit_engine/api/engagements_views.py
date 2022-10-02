import enum
import datetime

from django.db.models import Q
from django.core import serializers as dj_serializers
from rest_framework import exceptions, status, generics, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView

from configuration import models as config_models
from audit_engine.api.api_helpers import SerializeColumn, getUserCompany, getValidatedParams, getEngagementById
from audit_engine.api.validations import auditCreationValidation


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


class AuditSerializer:
    '''Used to generate a class to parse audit response.'''

    class Fields(enum.Enum):
        '''Class provides autocompletion in code editors.'''

        CompanyId = 'CompanyId'
        CompanyName = 'CompanyId'
        AuditId = 'AuditId'
        AuditName = 'AuditName'
        AuditType = 'AuditType'
        AuditStatus = 'AuditStatus'
        AuditScore = 'AuditScore'
        ClientType = 'ClientType'
        ClientTypeId = 'ClientTypeId'
        Channels = 'Channels'
        ChannelCount = 'ChannelCount'
        StartTime = 'StartTime'
        EndTime = 'EndTime'

    @classmethod
    def generateSerializer(cls, fields=None, exclude_fields=None):
        # If no field is passed select all fields to send response for.
        if not fields:
            fields = cls.Fields.__members__.values()

        # remove excluded fields.
        if exclude_fields:
            fields = list(filter(lambda x: x not in exclude_fields, fields))

        field_names = list(map(lambda x: x.name, fields))

        class BaseSerializer(serializers.ModelSerializer):
            for field in field_names:
                locals()[field] = serializers.SerializerMethodField()

            class Meta:
                model = config_models.Engagement
                fields = field_names

            def get_CompanyId(self, engagement):
                return engagement.company.id

            def get_CompanyName(self, engagement):
                return engagement.company.name

            def get_AuditName(self, engagement):
                # return f'{engagement.type} Audit'
                return engagement.name

            def get_AuditId(self, engagement):
                return f'{engagement.id}'

            def get_AuditType(self, engagement):
                return engagement.type

            def get_ClientType(self, engagement):
                return engagement.client_type.name

            def get_ClientTypeId(self, engagement):
                return engagement.client_type.id

            def get_AuditStatus(self, engagement):
                # is_open = engagement.end_Date - datetime.datetime.now(datetime.timezone.utc)
                # status = 'Open' if is_open.total_seconds() > 0 else 'Close'
                audit_status = 'Open' if engagement.is_active else 'Closed'
                return audit_status

            def get_Channels(self, engagement):
                # query for all channels present in the audit.
                channels = config_models.Channel.objects.filter(engagement=engagement)
                serializer = AllChannelsSerializer(channels, many=True)
                return serializer.data

            def get_ChannelCount(self, engagement):
                return config_models.ChannelType.objects.filter(engagement=engagement).count()

            def get_AuditScore(self, engagement):
                return engagement.compliance_score

            def get_StartTime(self, engagemet):
                return engagemet.start_Date

            def get_EndTime(self, engagemet):
                return engagemet.end_Date

        return BaseSerializer


@api_view(['GET'])
def getAllAudits(request):
    input_fields = [SerializeColumn(name='CompanyId')]
    validated_data = getValidatedParams(input_fields, request)
    company_id = [validated_data[key] for key in input_fields.keys()]
    allEngagemnets = config_models.Engagement.objects.filter(Q(company__id=company_id))
    Serializer = AuditSerializer.generateSerializer(exclude_fields=[AuditSerializer.Fields.AuditType,
                                                                    AuditSerializer.Fields.ClientType,
                                                                    AuditSerializer.Fields.ClientTypeId,
                                                                    AuditSerializer.Fields.StartTime,
                                                                    AuditSerializer.Fields.EndTime])
    json_response = Serializer(allEngagemnets, many=True).data
    return Response(json_response)


@api_view(["GET"])
def viewAuditSummary(request):
    input_fields = [SerializeColumn(name='CompanyId'),
                    SerializeColumn(name="AuditId")]

    validated_data = getValidatedParams(input_fields, request)
    company_id, audit_id = [validated_data[key] for key in input_fields.keys()]

    audit = config_models.Engagement.objects.filter(Q(company__id=company_id) & Q(id=audit_id))
    if len(audit) > 1:
        raise Exception('Multiple results for single audit. Check for internal errors.')

    audit = audit.first()
    Serializer = AuditSerializer.generateSerializer(exclude_fields=[AuditSerializer.Fields.AuditType,
                                                                    AuditSerializer.Fields.ClientType,
                                                                    AuditSerializer.Fields.ClientTypeId,
                                                                    AuditSerializer.Fields.StartTime,
                                                                    AuditSerializer.Fields.EndTime])
    json_response = Serializer(audit).data
    return Response(json_response)


@api_view(["POST"])
def addAudit(request):
    input_fields = [SerializeColumn('CompanyId', fieldType = serializers.UUIDField, db_column_name='company'),
                    SerializeColumn('AuditName', db_column_name='name'),
                    SerializeColumn('ClientType', db_column_name='client_type'),
                    SerializeColumn('AuditType', db_column_name='type'),
                    SerializeColumn('StartTime', fieldType=serializers.DateField, db_column_name='start_Date'),
                    SerializeColumn('EndTime', fieldType=serializers.DateField, db_column_name='end_Date'),
                    ]
    validated_data = getValidatedParams(input_fields, request)
    print(validated_data)
    # Logical validations before creating a new audit.
    # Also contains code to override validated_data for ForeignKey Records.
    success, response = auditCreationValidation(validated_data)
    if not success:
        return response

    audit = config_models.Engagement.objects.create(**response)
    Serializer = AuditSerializer.generateSerializer(exclude_fields=[
        AuditSerializer.Fields.CompanyId,
        AuditSerializer.Fields.CompanyName,
        AuditSerializer.Fields.AuditScore,
        AuditSerializer.Fields.Channels,
        AuditSerializer.Fields.ChannelCount

    ])
    json_response = Serializer(audit).data
    return Response(json_response)


class createEngagement(CreateAPIView):
    serializer_class = EngagementSerializer

    def create(self, request):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated

        company = getUserCompany(request)
        if not company:
            raise Exception('Developer Error!!! All user should contain company')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)
        return Response(serializer.data)


@ api_view(["POST"])
def deleteEngagement(request):
    fetched, result = getEngagementById(request)
    if not fetched:
        return result
    result.delete()
    return Response('Engagement Deleted')


@ api_view(["POST"])
def editEngagement(request):
    serializer = EngagementSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    fetched, result = getEngagementById(request)
    if not fetched:
        return result
    new_engagement = result.update(**serializer.validated_data)
    return dj_serializers.serialize('json', new_engagement)


@ api_view(['GET'])
def companyEngagements(request):
    if not request.user.is_authenticated:
        raise exceptions.NotAuthenticated
    company = getUserCompany(request)

    if not company:
        raise Exception('Developer Error!!! All user should contain company')

    allEngagemnets = config_models.Engagement.objects.filter(company=company)
    serializer = AuditResponseSerializer(allEngagemnets, many=True)
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
