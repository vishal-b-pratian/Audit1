from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers as config_serializers
from configuration import models as config_models
from django.contrib.auth import models as auth_models


@api_view(["GET"])
def getRoutes(request):
    """
    Method : get

    Function generates the routes for all the apis registered in the app configuration.
    """

    routes = [
        {"GET", "/api/users/"},
        {"GET", "/api/users/<int:id>/"},
        {"GET", "/api/company-details/"},
        {"GET", "/api/company-details/<uuid:id>/"},
        {"GET / POST", "/api/create-channel/"},
        {"GET / POST", "/api/create-channel-data/"},
        {"GET", "/api/engagement-details/"},
        {"PATCH", "/api/activate-channel/"},
        {"PATCH", "/api/inactivate-channel/"},
        {"PATCH", "/api/activate-channel-type/"},
        {"PATCH", "/api/inactivate-channel-type/"},
        {"GET", "/api/view-message-architecture-content/"},
        {"POST", "/api/add-channel-name"}
    ]


    return Response(routes)


@api_view(["GET"])
def getUsersData(request):
    """
    Method : get

    API returns the User data in the :model: 'models.auth.User'
    """

    users = auth_models.User.objects.all()
    serializer = config_serializers.UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getCompanyDetailsData(request):
    """
    Method : get

    Returns the details of all the registered companies in the :model: 'models.CompanyDetails'
    """
    sample_data = request.data.get('sample')
    # print(sample_data)
    company_details = config_models.CompanyDetails.objects.all()
    serializer = config_serializers.CompanyDetailsSerializer(company_details, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getEngagementDetails(request,company_id):
    """
    Method : Get

    Returns the engagement details of a particular company by taking in company id as a URL parameter.
    """

    response = {}

    # getting object of the company using company id
    company = config_models.CompanyDetails.objects.get(id = company_id)

    # querying based on comapny object
    engagement_details = config_models.Engagement.objects.filter(company = company)

    for engagement in engagement_details:
        channel_types_list=[]
        response['engagement'] = engagement.type
        channel_types = config_models.ChannelType.objects.filter(engagement=engagement)

        for channel_type in channel_types.values():
            channel_types_list.append(channel_type['channel_type'])
            response['channel-types'] = channel_types_list

        response['channel_type_count'] = len(response['channel-types'])

        for channel_type in channel_types:
            channels = config_models.Channel.objects.filter(type_name = channel_type)
            channel_list = []
            parameters_list = []

            for channel in channels.values():
                parameters = config_models.ChannelSourceParameter.objects.filter(channel=channel['id'])
                
                for parameter in parameters.values():
                    audit_parameter = config_models.AuditParameter.objects.get(id = parameter['parameters_id'])
                    print(audit_parameter)
                    parameters_list.append([audit_parameter.parameter,parameter['weight']])

                channel_list.append([channel['id'],channel['channel_title'],channel['is_active'],parameters_list])
                response[str(channel_type)]= {str(channel['channel_name_id']):channel_list}

    return Response(response)



@api_view(["GET"])
def getUrlDetailsChannelType(request,company_name, engagement_type, channel_type):
    """
    Method : Get

    Returns the url details of a particular company by taking in company name and engagement type as the URL parameters.
    """

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
    """
    Method : Get

    Returns the url details of a particular company by taking in company name and engagement type and channel name as the URL parameters.
    """

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
    """
    Method : Get

    Returns the channel details of a particular company by taking in company name as a URL parameter.
    """

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


@api_view(["GET"])
def viewAllSources(request, company_id):
    """
    Method : Get

    Returns the source details of a particular company by taking in company id as a URL parameter.
    """

    response = {}
    company_details = config_models.CompanyDetails.objects.get(id = company_id)
    if company_details:
        response['company_id'] = company_id
    engagement_details = config_models.Engagement.objects.filter(company = company_details)
    sources = []
    source_id = []
    channel_type_id = []
    channel_type_name = []
    source_status = []
    
    for engagement in engagement_details:
        url = config_models.Channel.objects.filter(engagement = engagement)
        for i in url:
            if i.url:
                source_id.append(str(i.id))
                sources.append(i.url)
                channel_type_id.append(i.type_name.id)
                channel_type_name.append(i.type_name.channel_type)
                source_status.append(i.is_active)

    for i in range(len(source_id)):
        response[source_id[i]] = {}
        response[source_id[i]]["url"] = sources[i]
        response[source_id[i]]["channel_type_id"] = channel_type_id[i]
        response[source_id[i]]["channel_type"] = channel_type_name[i]
        response[source_id[i]]["status"] = source_status[i]

    return Response(response)


@api_view(["GET"])
def viewSourcebyID(request, company_id, source_id):
    """
    Method : Get

    API return the source details of a particular company and a particular channel by taking the company id and source id as the URL parameters.
    """

    response = {}
    company_details = config_models.CompanyDetails.objects.get(id = company_id)
    if company_details:
        response['company_id'] = company_id
    url = config_models.Channel.objects.get(id = source_id)

    if url:
        sources = url.url
        channel_type_id = url.type_name.id
        channel_type_name = url.type_name.channel_type
        source_status = url.is_active
    response[source_id] = {}
    response[source_id]["url"] = sources
    response[source_id]["channel_type_id"] = channel_type_id
    response[source_id]["channel_type"] = channel_type_name
    response[source_id]["status"] = source_status
    
    return Response(response)


@api_view(["POST"])
def addSource(request):
    """
    Method : Post

    API posts the source details in the database for a particular company and for a particular channel through the json POST request.

    json_format : {
        "company_id" : <str>,
        "engagement_id" : <str>,
        "channel_title" : <str>,
        "channel_name" : <str>,
        "channel_type" : <str>,
        "link" : <str>
    }
    """

    company_id = request.data.get("company_id")
    engagement_id = request.data.get("engagement_id")
    channel_title = request.data.get("title")
    channel_name = request.data.get("channel_name")
    channel_type = request.data.get("channel_type")
    url = request.data.get("link")

    company = config_models.CompanyDetails.objects.get(id=company_id)
    engagement = config_models.Engagement.objects.get(id=engagement_id)

    config_models.ChannelType.objects.update_or_create(
        channel_type=channel_type,
        engagement=engagement,
    )

    channel_type_object = config_models.ChannelType.objects.get(
        channel_type=channel_type, 
        engagement=engagement
    )

    config_models.ChannelName.objects.update_or_create(
        channel_type_name=channel_type_object,
        channel_name=channel_name,
    )

    channel_name_object = config_models.ChannelName.objects.get(
        channel_name=channel_name,
        channel_type_name=channel_type_object
    )

    config_models.Channel.objects.create(
        channel_name=channel_name_object,
        type_name=channel_type_object,
        channel_title=channel_title,
        engagement=engagement,
        url=url,
    ).save()

    return Response("Successful")


@api_view(["PUT"])
def editSource(request):
    """
    Method : Put

    API edits the source details in the database for a particular company and for a particular channel through the json POST request.

    json_format : {
        "company_id" : <str>,
        "engagement_id)" : <str>,
        "channel_title" : <str>,
        "channel_name" : <str>,
        "channel_type" : <str>,
        "url" : <str>
    }
    """

    company_id = request.data.get("company_id")
    engagement_id = request.data.get("engagement_id")
    channel_title = request.data.get("title")
    channel_name = request.data.get("channel_name")
    channel_type = request.data.get("channel_type")
    url_id = request.data.get("link_id") 
    url = request.data.get("link")

    company = config_models.CompanyDetails.objects.get(id=company_id)
    engagement = config_models.Engagement.objects.get(id=engagement_id)

    config_models.ChannelType.objects.update_or_create(
        channel_type=channel_type,
        engagement=engagement,
    )

    channel_type_object = config_models.ChannelType.objects.get(
        channel_type=channel_type, 
        engagement=engagement
    )

    config_models.ChannelName.objects.update_or_create(
        channel_type_name=channel_type_object,
        channel_name=channel_name,
    )

    channel_name_object = config_models.ChannelName.objects.get(
        channel_name=channel_name,
        channel_type_name=channel_type_object
    )

    config_models.Channel.objects.filter(
        id = url_id
    ).update(
        channel_name=channel_name_object,
        channel_title=channel_title,
        type_name=channel_type_object,
        engagement=engagement,
        url=url,
    )

    return Response("Successful") 


@api_view(["POST"])
def addChannelType(request,engagement_id):
    """
    Method : Post

    API posts the channel type in the database for a particular engagement through the json POST request.

    json_format : {
        "channel_type_name" : <str>,
        "channel_type_weightage" : <str>
    }
    """

    channel_type = request.data.get('channel_type')
    response = {}

    channel_type_name = channel_type['channel_type_name']
    channel_type_weightage = channel_type['channel_type_weightage']
    engagement = config_models.Engagement.objects.get(id=engagement_id)
    channel_type_object = config_models.ChannelType.objects.create(
    channel_type=channel_type_name,
    engagement=engagement,
    channel_type_weightage= float(channel_type_weightage)
    ).save()
    response['channel_type'] = channel_type_object
    return Response(response)


@api_view(["POST"])
def addChannelName(request,channel_type_id):
    """
    Method : Post

    API posts the channel name in the database for a particular channel type through the json POST request.

    json_format : {
        "channel_name" : <str>
    }
    """

    channel_name = request.data.get("channel_name")
    channel_type_object = config_models.ChannelType.objects.get(
    id=channel_type_id
    )
    channel_name_created = config_models.ChannelName.objects.create(channel_type_name = channel_type_object,channel_name=channel_name).save()
    print(channel_name_created)
    return Response("succesful")


@api_view(["PATCH"])
def activateChannel(request):
    """
    Method : Patch

    API edits the status of channel in the database for a particular channel through the json POST request.

    json_format : {
        "Channel Id" : <str>
    }
    """
    channel_details = config_models.Channel.objects.filter(id = request.data.get('Channel Id')).update(is_active = True)
    response = "Message Channel Activated"
    return Response(response)  


@api_view(["PATCH"])
def inactivateChannel(request):
    """
    Method : Patch

    API edits the status of channel in the database for a particular channel through the json POST request.

    json_format : {
        "Channel Id" : <str>
    }
    """
    channel_details = config_models.Channel.objects.filter(id = request.data.get('Channel Id')).update(is_active = False)
    response = "Message Channel Inactivated"
    return Response(response) 


@api_view(["PATCH"])
def activateChannelType(request):
    """
    Method : Patch

    API edits the status of channel type in the database for a particular channel through the json POST request.

    json_format : {
        "ChannelType Id" : <str>
    }
    """

    channel_details = config_models.ChannelType.objects.filter(id = request.data.get('ChannelType Id')).update(is_active = True)
    response = "ChannelType Activated"
    return Response(response)


@api_view(["PATCH"])
def inactivateChannelType(request):
    """
    Method : Patch

    API edits the status of channel type in the database for a particular channel through the json POST request.

    json_format : {
        "ChannelType Id" : <str>
    }
    """

    channel_details = config_models.ChannelType.objects.filter(id = request.data.get('ChannelType Id')).update(is_active = False)
    response = "ChannelType Inactivated"
    return Response(response)


@api_view(['GET'])
def viewChannelTypes(request,engagement_id):
    """
    Method : Get

    Returns the channel type details of a particular engagement by taking in engagement id as a URL parameter.
    """
    response = {}
    engagement = config_models.Engagement.objects.get(id=engagement_id)
    channel_type = config_models.ChannelType.objects.filter(engagement=engagement)
    print(channel_type)
    response["engagement_id"] = engagement_id
    response[engagement.type] = {}
    list=[]
    # response[engagement.type]["channel_type"] = {}
    #  8b1deba3-37f3-4cc5-9f42-3d25cae663ac
    for i in channel_type:
        # print(i)
        list.append(i.channel_type)
        # response[engagement.id][] =
    response[engagement.type]["channel_type"] = list
    return Response(response)


@api_view(["GET"])
def viewMessageArchitectureContent(request, engagement_id):
    """
    Method : Get

    Returns the message architecture details of a particular engagement by taking in engagement id as a URL parameter.
    """

    response = {}
    engagement = config_models.Engagement.objects.get(id = engagement_id)
    auditparameter = config_models.AuditParameter.objects.filter(engagement = engagement)
    response[engagement.type] = {}
    for i in auditparameter:
        print(i)
        response[engagement.type][i.parameter] =   {}
        response[engagement.type][i.parameter]["keyword"] = i.keyword
        response[engagement.type][i.parameter]["parameter_content"] = i.parameter_content
    return Response(response)