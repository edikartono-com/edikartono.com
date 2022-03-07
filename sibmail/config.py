from json import dumps
from requests import request
import sib_api_v3_sdk
from sib_api_v3_sdk import Configuration
from sib_api_v3_sdk.rest import ApiException
from sibmail.models import SibAccount

def configure(*sdk):
    account = SibAccount.objects.last()
    if account:
        configuration = Configuration()
        configuration.api_key['api-key'] = account.api_key
        for s in sdk:
            api_instance = s(
                sib_api_v3_sdk.ApiClient(configuration)
            )
        return api_instance

def url_response():
    url = "https://api.sendinblue.com/v3/account"
    headers = {
        "Accept": "application/json",
        "api-key": configure()
    }
    response = request('GET', url, headers=headers)
    return {"error": response.text}

def get_sib_account():
    api_instance = configure(sib_api_v3_sdk.AccountApi)
    if api_instance:
        context = api_instance.get_account()
    else:
        context = url_response()
    return context

def get_sib_contact(**kwargs):
    api_instance = configure(sib_api_v3_sdk.ContactsApi)
    if api_instance:
        api_response = api_instance.get_contacts(**kwargs)
        context = dumps(api_response.contacts)
    else:
        context = url_response()
    return context

def get_contact_details(email):
    api_response = configure(sib_api_v3_sdk.ContactsApi)
    if api_response:
        context = api_response.get_contact_info(email)
    else:
        context = url_response()
    return context

def get_email_campaigns(**options):
    api_instance = configure(sib_api_v3_sdk.EmailCampaignsApi)
    try:
        api_response = api_instance.get_email_campaigns(**options)
        context = dumps(api_response)
    except ApiException:
        context = url_response()
    return context