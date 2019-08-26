# django imports
from rest_framework import serializers



class UpdatePageInfoSerializer(serializers.Serializer):


    page_id         = serializers.CharField()
    access_token    = serializers.CharField()
    update_data     = serializers.DictField()
