# django imports
from django.shortcuts import render

from allauth.socialaccount.models import SocialToken

import facebook

# default index view
def index(request):
    return render(request, "index.html", {})
