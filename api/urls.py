# Django imports
from django.urls import path

# REST imports
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
# REST swagger imports

from rest_framework_swagger.views import get_swagger_view

# local imports
from api import views

urlpatterns = [

    # API Django doc
    path('', include_docs_urls(title='facebook_app API', public=True)),

    # API swagger doc
    path('swagger/', get_swagger_view(title='facebook_app API')),

    # scheme view
    path('schema/', get_schema_view(title="facebook_app API"), name="schema_view"),
    #
    # # GET average_price for each day
    path('pages/', views.pages, name="pages"),

    # # GET average_price null for less than 3 prices
    path('page_details/<str:page_id>/', views.page_details, name="page_details"),

    # POST upload_price
    path('update_page/', views.UpdatePageInfoViewSet.as_view(), name="update_page"),

    # /accounts/facebook/login/

]
