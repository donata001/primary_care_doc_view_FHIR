from rest_framework import serializers
from my_app.models import Publisher


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ('id', 'name', 'address', 'city', 'state_province', 'country', 'website')
        