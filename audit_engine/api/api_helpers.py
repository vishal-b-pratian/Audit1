from rest_framework import status
from rest_framework.response import Response
from configuration import models as config_models


def getUserCompany(request, validate=True):
    '''Helps to simulate request even if user is not logged in. As Frontend is angular and auth
    will take place with azure AD, validate=False will return some company if available.'''
    if validate:
        return request.user.company
    return config_models.CompanyDetails.objects.all().first()


def getEngagementById(request):
    _id = request.GET.get('id', None) if request.method == "GET" else request.data.get('id', None)
    if not _id:
        return False, Response('Engagement Id is Required', status=status.HTTP_400_BAD_REQUEST)

    engagement = config_models.Engagement.objects.filter(id=_id).first()
    if not engagement:
        return False, Response('Engagement not found',
                               status=status.HTTP_400_BAD_REQUEST)

    return True, engagement


def instanseNotFoundResponse(class_name, parameter='parameter'):
    return Response(f"Couldn't find isntance for {class_name}. Please ensure correct {parameter} is passed in quety",
                    status=status.HTTP_400_BAD_REQUEST)
