from rest_framework import serializers
from events.models import SSLCommerzDatum


class SSLCommerzDatumSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSLCommerzDatum
        fields = "__all__"
        read_only_fields = ["order"]
