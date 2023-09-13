from rest_framework import serializers


class MailingSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    subject = serializers.CharField()
    message = serializers.CharField()
    filter = serializers.CharField(required=False)
    template_name = serializers.CharField(required=False)


class MailingIdSerializer(serializers.Serializer):
    mailing_id = serializers.IntegerField()


class MailingUpdateMethodSerializer(serializers.Serializer):
    mailing_id = serializers.IntegerField()
    data = serializers.JSONField()
