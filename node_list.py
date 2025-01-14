import requests


def get_connected_peers(api_url):
    """Get the list of connected peers from the IPFS API."""

    url = f"{api_url}/api/v0/swarm/peers"
    response = requests.post(url)
    return response.json()


def main():

    api_url = "http://localhost:5001"

    try:
        peers_info = get_connected_peers(api_url)
        peers = peers_info.get("Peers", [])

        unique_peers = {}

        for peer in peers:
            peer_id = peer.get("Peer")
            address = peer.get("Addr")

            unique_peers[peer_id] = address

        print(f"Connected peers for node at {api_url}:")
        for peer_id, address in unique_peers.items():
            print(f"Peer ID: {peer_id}")
            print(f"Address: {address}")
            print("-" * 40)

    except Exception as e:
        print(f"Error fetching connected peers from {api_url}: {e}")


if __name__ == "__main__":
    main()
