from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers as config_serializers
from configuration import models as config_models
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
