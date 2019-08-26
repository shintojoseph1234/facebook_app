
# REST imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView

# ALLauth imports
from allauth.socialaccount.models import SocialToken

# local imports
from api.serializers import *

# # other imports
import requests
import facebook


def get_error_message(error_type, message):
    '''
    Checks the error type and message,
    and returns error message with error code
    Parameters:
        error_type (str)    : The error type.
        message (dict)      : The response message from serializer.
    Returns:
        list: returns error message with error code
    '''

    if error_type == "DATA_ERROR":

        error_status = [{
                        "status": "error",
                        "data": {
                            "http_code": "400 BAD REQUEST",
                            "errors": [{
                                "error_code": 2000,
                                "error_message": message
                                }]
                            }
                        }]
        return Response(error_status, status=status.HTTP_400_BAD_REQUEST)

    else:
        error_status = [{
            "status": "error",
            "data": {
                "http_code": "500 INTERNAL SERVER ERROR",
                "errors": [{
                    "error_code": 2003,
                    "error_message": "Unknown Internal server error"
                    }]
                }
            }]

    return Response(error_status, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def pages(request, access_token):
    '''
    List of pages user owns.

    Returns:
        list: returns a list of pages user owns.
    '''

    # try
    try:
        # pass the access_token to GraphAPI
        graph = facebook.GraphAPI(access_token=access_token)
        # find the datas available on request for the user
        pages_data = graph.get_object("/me/accounts")
        # initialize and empty response list
        response_list = []
        # if pages_data is not empty
        if pages_data:
            # for each page details in pages_data
            for each_page in pages_data['data']:
                # create a empty dictionary
                response_dict = {}
                # save category into response_dict
                response_dict['category'] = each_page['category']
                # save name into response_dict
                response_dict['name'] = each_page['name']
                # save id into response_dict
                response_dict['id'] = each_page['id']
                # append page info to response_list
                response_list.append(response_dict)

        else:
            # initialize a empty dictionary
            response_dict = {}
            # set category as None
            response_dict['category'] = None
            # set name as None
            response_dict['name'] = None
            # set id as None
            response_dict['id'] = None
            # append to response_list
            response_list.append(response_dict)
    except:
        # initialize and empty response list
        response_list = []


    # success response
    success = [{
                "status": "success",
                "data": response_list
                }]

    return Response(success, status=status.HTTP_200_OK)


@api_view(['GET'])
def page_details(request, page_id, access_token):
    '''
    Details of single page user owns.

    Parameters:
        page_id (str)  : Id of the page.

    Returns:
        list: returns details of the page.
    '''

    try:
        # initialize and empty response list
        response_list = []
        # pass the access_token to GraphAPI
        graph = facebook.GraphAPI(access_token=access_token)
        # find the datas available on request for the user
        pages_data = graph.get_object("/me/accounts")
        # set page_access_token as none
        page_access_token = None
        # for each_page details search matching id
        for each_page in pages_data['data']:
            # find th matching page id
            if each_page['id'] == page_id:
                # obtain the access token
                page_access_token = each_page['access_token']

        # pass the access_token to GraphAPI
        graph = facebook.GraphAPI(access_token=page_access_token)
        # fields to obtain details from page
        field_list = '''  phone,
                          location,
                          about,
                          emails,
                          category_list,
                          company_overview,
                          contact_address ,
                          description,
                          impressum,
                          is_permanently_closed'''
        # obtain the page detail
        page_details = graph.get_object(id=str(page_id), fields=field_list )
        # append page_details to response_list
        response_list.append(page_details)
    except:
        # initialize and empty response list
        response_list = []

    # success response
    success = [{
                "status": "success",
                "data": response_list
                }]
    return Response(success, status=status.HTTP_200_OK)



class UpdatePageInfoViewSet(GenericAPIView):
    """
    API endpoint where you can upload a list of prices between
    date_from and date_to

    Parameters:
        price (list)            : The list of integer prices.

    Returns:
        list: returns a success or failure message
    """

    queryset = ''
    serializer_class = UpdatePageInfoSerializer

    def post(self, request, *args, **kwargs):

        # obtain the data
        data = request.data
        # check data with serializer
        serializer = UpdatePageInfoSerializer(data=data)
        # if serialiser not valid
        if not serializer.is_valid():
            # return error message
            return get_error_message("DATA_ERROR", str(serializer.errors))

        # inputs from API
        page_id              = data['page_id']
        access_token         = data['access_token']
        update_data          = data['update_data']

        # pass the access_token to GraphAPI
        graph = facebook.GraphAPI(access_token=access_token)
        # find the datas available on request for the user
        pages_data = graph.get_object("/me/accounts")
        # set page_access_token as none
        page_access_token = None
        # for each_page details search matching id
        for each_page in pages_data['data']:
            # find th matching page id
            if each_page['id'] == page_id:
                # obtain the access token
                page_access_token = each_page['access_token']

        # include token to update_data to post
        update_data['access_token'] = page_access_token
        # url to post the data with our page_id
        url = 'https://graph.facebook.com/{}'.format(str(page_id))
        # header to include in post request
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        # obtain the response
        response = requests.post(url, data=update_data, headers=headers)
        # if status success
        if response.status_code == 200:
            # set status_code as 200 ok
            status_code = status.HTTP_200_OK
            # success message
            message = "success"

        else:
            # set status_code as failed
            status_code = status.HTTP_204_NO_CONTENT
            # failure message
            message = "failure"

        # response
        success = [{
                    "status": message
                   }]

        return Response(success, status=status_code)
