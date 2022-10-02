import datetime
from rest_framework.response import Response
from rest_framework import status
from configuration import models as config_models
from audit_engine.api.api_helpers import instanseNotFoundResponse


def auditCreationValidation(data):
    company_id = data['company']
    audit_name = data['name'].strip()  # remove starting and trailing spaces.
    client_type = data['client_type']
    audit_type = data['type']  # take care of audit type case.
    start_date = data['start_Date']
    end_date = data['end_Date']

    audit_type_values = list(map(lambda x: x[1], config_models.PREDEFINED_AUDIT_TYPES))
    company_object = config_models.CompanyDetails.objects.filter(id = company_id).first()
    
    # company should exists
    if not company_object:
        return False, instanseNotFoundResponse('Company', 'CompanyId')
    data['company'] = company_object

    # AuditName should not be empty.
    if not audit_name:
        return False, Response("AuditName can't be empty.")

    # Client Type should already exist in the table
    client_type_object = config_models.ClientType.objects.filter(name=client_type).first()
    if not client_type:
        return False, instanseNotFoundResponse('ClientType')
    data['client_type'] = client_type_object 

    # AuditType should already be defined
    # Directly validating from code as no seperate table is being used.
    if audit_type not in audit_type_values:
        return False, instanseNotFoundResponse('AuditType', 'AuditType')

    # Same company should not have multiple similar audit type
    company_audits_count= config_models.Engagement.objects.filter(company = company_object, type = audit_type).count()
    if company_audits_count:
        return  False, Response("Cannot create multiple audits with same audit type within a company.", status=status.HTTP_400_BAD_REQUEST)

    if datetime.datetime.now().date() > start_date:
        return False, Response("StartDate can't be less than today's date.", status=status.HTTP_400_BAD_REQUEST)

    if datetime.datetime.now().date() > end_date:
        return False, Response("StartDate can't be less than today's date.", status=status.HTTP_400_BAD_REQUEST)

    return True, data
