from rest_framework import serializers
from core.models import Tags


class TagSerializer(serializers.ModelSerializer):
    """ serializer for tag objects """

    class Meta:
        model = Tags
        fields = ('id', 'name')
        read_only = ('id',)
