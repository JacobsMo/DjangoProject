from rest_framework import serializers


class StripeSessionCreationSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
