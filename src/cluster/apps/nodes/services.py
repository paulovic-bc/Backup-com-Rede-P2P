import requests
from rest_framework.exceptions import ValidationError


class ActiveNodeService:

    def _get_connected_peers(node_ip):
        """Get the list of connected peers from the IPFS node."""

        url = f"{node_ip}/api/v0/swarm/peers"
        response = requests.post(url)
        return response.json()

    def get_active_nodes(self) -> list[dict[str, str]]:

        url = "http://localhost:5001/api/v0/swarm/peers"

        response = requests.post(url)

        if response.status_code == 200:
            peers_info = response.json()
            peers = peers_info.get("Peers", [])
            active_nodes = []

            for peer in peers:
                peer_id = peer.get("Peer")
                address = peer.get("Addr")
                active_nodes.append({"peer_id": peer_id, "address": address})

            return active_nodes
        else:
            raise ValidationError(detail={"node": f"{response.text}."}, code="invalid")
