# Contains API used by internal services.
from django.core import serializers as dj_serializers
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView

from audit_engine.api import api_helpers
from rest_framework import serializers, status
from configuration import models as config_models
from audit_engine import models as audit_models
from content_management import models as content_models


@api_view('GET')
def triggerScoreGeneration(request):
    '''Should be trigged by the content service to start score card generation.'''
    channelId = request.GET.get('ChannelId', None)
    # validate channel Id
    if not channelId:
        return Response('ChannelId parameter not found.', status=status.HTTP_400_BAD_REQUEST)
    
    # get channel from channel Id
    channel = config_models.Channel.objects.filter(id=channelId).first()
    
    if not channel:
        return api_helpers.instanseNotFoundResponse(class_name='Channel', parameter='channelId')

    # get mapped_keyword in json format
    mapped_keywords = content_models.MappedKeyWords.objects.filter(channel=channel).first()

    if not mapped_keywords:
        return api_helpers.instanseNotFoundResponse(class_name='Channel', parameter='channelId')

    mapped_keywords = mapped_keywords.mapped_keywords
    
    # multiple parameters are available for a single channel. Merge SQL and JSON paramters.
    # config and content services Models are not compatable with each other.

    channelSourceParameter = config_models.ChannelSourceParameter.objects.query(channel=channel)
    for sourceParameter in channelSourceParameter:
        parameter_name =  sourceParameter.parameters.parameter
        assert parameter_name in mapped_keywords
        mapped_keywords[parameter_name]['count']
        # if parameter_name not in 
        
        
        # audit_models.SourceParameterScore.objects.create(
        #     source = sourceParameter,
        #     keyword_count = ,
        #     keyword_frequencies = ,
        #     parameter_score = ,
        # )

