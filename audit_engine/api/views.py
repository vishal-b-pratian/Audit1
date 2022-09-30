import datetime
from statistics import mode
from time import time
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from audit_engine import models as audit_models
from audit_engine.api import serializers
from configuration import models as config_model



@api_view(["GET"])
def getRoutes(request):

    routes = {"GET": "/api/sdfskd"}

    return Response((routes))


@api_view(["GET"])
def getStatus(request):

    status = {
        "In progress": 0,
        "Completed": 0,
    }

    audits = audit_models.AuditInformation.objects.all()

    for audit in audits:
        if audit.end_date > datetime.now().date():
            status["In progress"] += 1
        else:
            status["Completed"] += 1

    return Response(status)


@api_view(["GET"])
def getOverallScore(request):

    audits = audit_models.AuditInformation.objects.all()
    score_avg = 0.0
    for audit in audits:
        score_avg += audit.overall_compliance_score

    score_avg = (score_avg * 100) / len(audits)

    api_response = {"compliance score": score_avg}

    return Response((api_response))


class getEngagements(ListAPIView):
    queryset = config_model.Engagement.objects.all()
    serializer_class = serializers.EngagementsSerializer

