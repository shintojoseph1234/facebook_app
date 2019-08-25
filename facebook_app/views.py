# django imports
from django.shortcuts import render

from allauth.socialaccount.models import SocialLogin, SocialToken, SocialApp

import facebook

# default index view
def index(request):

    print (str(request.user))
    # AnonymousUser
    if str(request.user) != "AnonymousUser":
        access_token = SocialToken.objects.get(account__user=request.user, account__provider='facebook') #get instead of filter (you need only one object)
        print (access_token)
        graph = facebook.GraphAPI(access_token=access_token)
        print (graph)
        pages_data = graph.get_object("/me/accounts")
        print (pages_data)

    return render(request, "index.html", {})
