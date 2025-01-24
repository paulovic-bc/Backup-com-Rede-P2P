from time import sleep

from core import settings
from django.db import transaction
from requests import post

from .models import Node


def convert_to_active_node_list(unique_peers: dict[str, str]) -> list[dict[str, any]]:
    active_nodes = []

    for peer_id, value in unique_peers.items():

        ip_protocol, ip_address, transport_protocol, port = (
            value.split("/")[1],
            value.split("/")[2],
            value.split("/")[3],
            value.split("/")[4],
        )

        active_node = {
            "name": peer_id,
            "ip_protocol": ip_protocol,
            "ip_address": ip_address,
            "transport_protocol": transport_protocol,
            "port": port,
            "network_type": "p2p",
            "peer_id": peer_id,
            "active": True,
        }

        active_nodes.append(active_node)

    return active_nodes


def update_status_nodes():
    while True:
        try:
            bootstrap_node_url = (
                f"http://{settings.BOOTSTRAP_NODE_HOST}:5001/api/v0/swarm/peers"
            )

            response = post(bootstrap_node_url)

            peers_info = response.json()
            peers = peers_info.get("Peers", [])
            unique_peers = {}

            for peer in peers:
                peer_id = peer.get("Peer")
                address = peer.get("Addr")

                unique_peers[peer_id] = address

            active_nodes = convert_to_active_node_list(unique_peers=unique_peers)

            with transaction.atomic():
                Node.objects.update(active=False)

                for active_node in active_nodes:
                    current_node = Node.objects.filter(
                        peer_id=active_node["peer_id"]
                    ).first()

                    if current_node:
                        current_node.active = True
                        current_node.save()
                    else:
                        Node.objects.create(**active_node)

                bootstrap_node = Node.objects.filter(
                    peer_id=settings.BOOTSTRAP_NODE_PEER_ID
                ).first()
                bootstrap_node.active = True
                bootstrap_node.save()

            sleep(30)
        except Exception as e:
            print(f"Error fetching connected peers from {bootstrap_node_url}: {e}")
