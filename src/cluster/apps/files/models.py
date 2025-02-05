from django.db.models import (
    CASCADE,
    PROTECT,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    Model,
)
from django.utils import timezone
from nodes.models import Node


class File(Model):
    node = ForeignKey(Node, on_delete=PROTECT, related_name="files")

    name = CharField(max_length=128)
    hash = CharField(max_length=128, unique=True)

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.hash}"


class FileVersion(Model):
    file = ForeignKey(File, on_delete=CASCADE, related_name="file_versions")

    hash = CharField(max_length=128)

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.hash}"
