from django.db.models import BooleanField, CharField, DateTimeField, Model
from django.utils import timezone


class Node(Model):
    name = CharField(max_length=128)
    ip_protocol = CharField(max_length=128)
    ip_address = CharField(max_length=128)
    transport_protocol = CharField(max_length=128)
    port = CharField(max_length=128)
    network_type = CharField(max_length=128)
    peer_id = CharField(max_length=128)
    active = BooleanField()

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name
