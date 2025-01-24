# PFS P2P Backup Network with Cluster API

This project sets up a private P2P backup network using IPFS (InterPlanetary File System). The network consists of several nodes (sectors), where devices upload their data. Due to the P2P nature of IPFS, all sectors in the network will have access to the uploaded data. The Cluster API is used to centralize the management of the nodes and facilitate operations such as CRUD for nodes, file uploads/downloads, and versioning of files.

## Features:

- **P2P Data Storage:** Data uploaded to any node (sector) is replicated across all other nodes in the network.
- **CRUD Operations for Nodes:** Manage IPFS nodes with centralized operations like adding, updating, and removing nodes.
- **File Upload/Download:** Devices can upload files to their respective sectors, and files are accessible across all sectors in the network.
- **Versioning:** Support for version control of uploaded files, allowing users to track changes and retrieve previous versions.

## Default Node Setup:

The project is configured to run with 3 IPFS nodes by default. These nodes represent sectors in the network, and they will replicate any data uploaded to them across all nodes.

If you need more nodes, you can easily add them by adding additional IPFS node containers to the docker-compose.yml file.

A sample configuration for a single-node setup is provided in the file **docker-compose-single-node.yml**, which includes just one IPFS node. You can use this as a template to add more nodes to your setup.

**Automatic Node Detection**: When a new node (container) is added to the network, the API automatically detects it and registers the node in the database.


## Steps to Run the Project

### 1. Clone the Repository
Start by cloning the repository to your local machine.

```bash
git clone https://github.com/paulovic-bc/Backup-com-Rede-P2P.git
cd Backup-com-Rede-P2P
```

### 2. Environment Configuration
The .env.docker file, which contains the necessary environment variables for the PostgreSQL database, is already included in the repository. No additional configuration is required.

### 3. Build and Start the Services
Once you have the repository, you can build and start the services using Docker Compose.

```bash
docker-compose up --build
```

This command will:

- Start the IPFS nodes (default 3 nodes, or more if added).
- Start the PostgreSQL database for managing node metadata.
- Start the Cluster API, which manages CRUD operations and file versioning.

### 4. Access the Services
Once the services are up and running, you can interact with the system:

#### IPFS Nodes:

- Node 1 (Sector A): http://localhost:5001
- Node 2 (Sector B): http://localhost:5002
- Node 3 (Sector C): http://localhost:5003

#### Cluster Backend API:

Access the Swagger API for managing nodes, uploading/downloading files, and versioning at http://localhost:8001/api/v1/swagger/.

#### PostgreSQL Database:

Connect to the database at localhost:5434 using any database client for managing node metadata.