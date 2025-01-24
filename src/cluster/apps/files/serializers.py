from nodes.models import Node
from nodes.serializers import NodeSerializer
from rest_framework.serializers import (
    CharField,
    FileField,
    ModelSerializer,
    PrimaryKeyRelatedField,
)

from .models import File, FileVersion


class FileVersionSerializer(ModelSerializer):
    path = FileField(write_only=True)
    hash = CharField(read_only=True)

    class Meta:
        model = FileVersion
        fields = ["id", "path", "hash"]


class FileSerializer(ModelSerializer):
    node_id = PrimaryKeyRelatedField(
        queryset=Node.objects.all(), write_only=True, source="node"
    )

    name = CharField(read_only=True)
    path = FileField(write_only=True)
    hash = CharField(read_only=True)

    node = NodeSerializer(read_only=True)
    file_versions = FileVersionSerializer(read_only=True, many=True)

    class Meta:
        model = File
        fields = ["id", "node_id", "name", "path", "hash", "node", "file_versions"]
