from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import NotFound
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from .filters import FileFilter
from .models import File
from .serializers import FileSerializer, FileVersionSerializer
from .services import FileService, handle_duplicate_hash


@extend_schema_view(
    create=extend_schema(
        summary="Upload a new file",
        description="Uploads a new file.",
    ),
    update=extend_schema(
        summary="Update a new file",
        description="Updates a new file.",
    ),
)
class FileViewSet(ModelViewSet):
    queryset = File.objects.all().order_by("-id")
    serializer_class = FileSerializer
    filterset_class = FileFilter
    parser_classes = (MultiPartParser,)
    http_method_names = ["get", "post", "put"]
    permission_classes = []
    service = FileService()

    def get_serializer_class(
        self,
    ) -> FileSerializer | FileVersionSerializer:
        if self.action == "update":
            return FileVersionSerializer
        return FileSerializer

    @transaction.atomic
    @handle_duplicate_hash
    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_data = self.service.create_file(
            serializer_data=serializer.validated_data,
        )

        return Response(file_data, status=HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs) -> Response:
        file = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_data = self.service.update_file(
            instance=file,
            serializer_data=serializer.validated_data,
        )

        return Response(file_data, status=HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        summary="Download a file by id",
        description="Downloads a file by id.",
    ),
)
class FileDownloadByIdViewSet(RetrieveAPIView):
    queryset = File.objects.all().order_by("-id")
    serializer_class = FileSerializer
    parser_classes = (MultiPartParser,)
    service = FileService()

    @transaction.atomic
    def retrieve(self, request: Request, id: int) -> Response:
        queryset = self.get_queryset()

        try:
            file = queryset.get(id=id)
        except File.DoesNotExist:
            raise NotFound()

        response_file = self.service.get_file_to_download(file=file)

        return response_file
