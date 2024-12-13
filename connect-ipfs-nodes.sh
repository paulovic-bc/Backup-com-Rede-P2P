#!/bin/bash

# Node 1 peer ID
NODE1_ID=$(docker exec ipfs-node1 ipfs id -f="<id>")

# Node 2 peer ID
NODE2_ID=$(docker exec ipfs-node2 ipfs id -f="<id>")

# Node 3 peer ID
NODE3_ID=$(docker exec ipfs-node3 ipfs id -f="<id>")

# Connect Node 2 to Node 1
docker exec ipfs-node2 ipfs swarm connect /ip4/192.168.1.101/tcp/4001/p2p/$NODE1_ID

# Connect Node 1 to Node 2
docker exec ipfs-node1 ipfs swarm connect /ip4/192.168.1.102/tcp/4001/p2p/$NODE2_ID

# Connect Node 3 to Node 1
docker exec ipfs-node3 ipfs swarm connect /ip4/192.168.1.101/tcp/4001/p2p/$NODE1_ID

# Connect Node 1 to Node 3
docker exec ipfs-node1 ipfs swarm connect /ip4/192.168.1.103/tcp/4001/p2p/$NODE3_ID

# Connect Node 3 to Node 2
docker exec ipfs-node3 ipfs swarm connect /ip4/192.168.1.102/tcp/4001/p2p/$NODE2_ID

# Connect Node 2 to Node 3
docker exec ipfs-node2 ipfs swarm connect /ip4/192.168.1.103/tcp/4001/p2p/$NODE3_ID

echo "Nodes have been successfully connected."
