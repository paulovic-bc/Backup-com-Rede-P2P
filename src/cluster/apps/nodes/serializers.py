from rest_framework.serializers import CharField, ModelSerializer, Serializer

from .models import Node


class NodeSerializer(ModelSerializer):

    class Meta:
        model = Node
        fields = [
            "id",
            "name",
            "ip_protocol",
            "ip_address",
            "transport_protocol",
            "port",
            "network_type",
            "peer_id",
            "active",
        ]


class ActiveNodeSerializer(Serializer):
    peer_id = CharField(max_length=255, required=True)
    address = CharField(max_length=255, required=True)
