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

def create_a_contact(email, list_id=5, **payload):
    api_instance = configure(sib_api_v3_sdk.ContactsApi)
    creating_contact = sib_api_v3_sdk.CreateContact(
        email=email,
        attributes=payload,
        email_blacklisted=False,
        sms_blacklisted=False,
        list_ids=[list_id],
        update_enabled=True
    )

    try:
        api_response = api_instance.create_contact(creating_contact)
        context = api_response
    except ApiException:
        context = url_response()
    return context

def create_doi_contact(email, success_url, list_id=5, **attr):
    api_instance = configure(sib_api_v3_sdk.ContactsApi)

    doi_contact = sib_api_v3_sdk.CreateDoiContact()
    doi_contact.email = email
    doi_contact.attributes = attr
    doi_contact.include_list_ids = [list_id]
    doi_contact.template_id = 1
    doi_contact.redirection_url = success_url

    try:
        api_instance.create_doi_contact(doi_contact)
    except ApiException:
        url_response()

def delete_contact(email):
    api_instance = configure(sib_api_v3_sdk.ContactsApi)

    try:
        api_instance.delete_contact(email)
    except ApiException:
        url_response()

def get_all_email_campaigns(**options):
    api_instance = configure(sib_api_v3_sdk.EmailCampaignsApi)
    try:
        api_response = api_instance.get_email_campaigns(**options)
        context = api_response
    except ApiException:
        context = url_response()
    return context

def get_all_folders(limit: int, offset: int, sorts: str):
    api_instance = configure(sib_api_v3_sdk.ContactsApi)
    try:
        api_response = api_instance.get_folders(limit, offset)
        context = api_response
    except ApiException:
        context = url_response()
    return context

def get_list_in_folder(folder_id: int, limit: int, offset: int = 0):
    api_instance = configure(sib_api_v3_sdk.FoldersApi)

    try:
        api_response = api_instance.get_folder_lists(folder_id, limit=limit, offset=offset)
        context = api_response
    except ApiException:
        context = url_response()
    return context