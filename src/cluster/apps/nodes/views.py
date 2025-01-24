from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ViewSet
from utils.viewsets import ProtectedDeleteViewSet

from .filters import NodeFilter
from .models import Node
from .serializers import ActiveNodeSerializer, NodeSerializer
from .services import ActiveNodeService


@extend_schema_view(
    list=extend_schema(
        summary="List all node",
        description="Returns a list of all node in the system with pagination.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific node",
        description="Returns a node by its ID.",
    ),
    create=extend_schema(
        summary="Create a new node",
        description="Creates a new node with the given details.",
    ),
    update=extend_schema(
        summary="Update a node",
        description="Updates a node's details by its ID.",
    ),
    partial_update=extend_schema(
        summary="Partially update a node",
        description="Partially updates a node's details by its ID.",
    ),
    destroy=extend_schema(
        summary="Delete a node", description="Deletes a node by its ID."
    ),
)
class NodeViewSet(ProtectedDeleteViewSet):
    queryset = Node.objects.all().order_by("-id")
    serializer_class = NodeSerializer
    filterset_class = NodeFilter
    permission_classes = []
    http_method_names = ["get", "post", "put", "patch"]
