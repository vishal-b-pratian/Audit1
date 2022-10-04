from utils import wait, pretty_print_response
import requests as rq
import urllib3
from utils import url, company_id, select_option
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PREDEFINED_AUDIT_TYPES = {"branding": "branding",
                          "positioning": "positioning",
                          "both": "both"
                          }


def render_home_screen_data():
    wait('Home Screen Demo')
    response = rq.get(url + 'companyAuditStatusSummary', params={'CompanyId': company_id},
                      verify=False)
    pretty_print_response(response)

    response = rq.get(url + 'companyAuditSummary', params={'CompanyId': company_id},
                      verify=False)
    pretty_print_response(response)


def home_screen_search():
    wait("Home screen Audit Search")
    audit_name = input('Input Search Query: ')
    response = rq.get(url + 'searchAudit', params={'CompanyId': company_id,
                                                   'AuditName': audit_name},
                      verify=False)
    pretty_print_response(response)


def home_screen_filter_audit():
    wait("Home screen Audit Filter")
    audit_type = select_option(PREDEFINED_AUDIT_TYPES, 'Audit Filter Type')
    response = rq.get(url + 'filterAudit', params={'CompanyId': company_id,
                                                   'AuditType': audit_type},
                      verify=False)
    pretty_print_response(response)


def demo_home_screen():
    render_home_screen_data()
    home_screen_search()
    home_screen_filter_audit()
demo_home_screen()