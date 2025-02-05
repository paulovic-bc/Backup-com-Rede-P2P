from collections import OrderedDict
from io import BytesIO
from os.path import basename

import requests
from core import settings
from django.db import IntegrityError
from django.http import FileResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import File, FileVersion
from .serializers import FileSerializer


def handle_duplicate_hash(view_func):
    def _wrapped_view(self, request, *args, **kwargs):
        try:
            return view_func(self, request, *args, **kwargs)
        except IntegrityError as e:
            if (
                'duplicate key value violates unique constraint "files_file_hash_key"'
                in str(e)
            ):
                return Response(
                    {"detail": "Duplicate hash value. File already exists."},
                    status=status.HTTP_208_ALREADY_REPORTED,
                )
            raise e

    return _wrapped_view


class FileService:

    def create_file(self, serializer_data: OrderedDict) -> dict[str, any]:
        node = serializer_data.get("node")

        if node.active == False:
            raise ValidationError(detail={"node": f"Node is inactive"}, code="inactive")

        file_path = serializer_data.get("path")
        file_name = basename(file_path.name)
        serializer_data["name"] = file_name

        content = serializer_data["path"].read()

        response = requests.post(
            f"http://{node.ip_address}:5001/api/v0/add", files={"file": content}
        )

        if response.status_code == 200:
            response_data = response.json()

            serializer_data["hash"] = response_data["Hash"]

            serializer_data.pop("path")

            file = File.objects.create(**serializer_data)

            file_data = FileSerializer(file).data

            return file_data
        else:
            raise ValidationError(detail={"path": f"{response.text}."}, code="invalid")

    def update_file(self, instance: File, serializer_data: OrderedDict) -> None:
        serializer_data["file"] = instance

        node = instance.node
        if node.active == False:
            raise ValidationError(detail={"node": f"Node is inactive"}, code="inactive")

        file_path = serializer_data.get("path")
        file_name = basename(file_path.name)

        if file_name != instance.name:
            raise ValidationError(
                detail={"path": "File name is different to original file name."},
                code="invalid",
            )

        content = serializer_data["path"].read()

        response = requests.post(
            f"http://{node.ip_address}:5001/api/v0/add", files={"file": content}
        )

        if response.status_code == 200:
            response_data = response.json()

            serializer_data["hash"] = response_data["Hash"]

            serializer_data.pop("path")

            FileVersion.objects.create(**serializer_data)

            file_data = FileSerializer(instance).data

            return file_data
        else:
            raise ValidationError(detail={"path": f"{response.text}."}, code="invalid")

    def get_file_to_download(self, file: File) -> FileResponse:

        lastest_file_version = (
            FileVersion.objects.filter(file_id=file.id).order_by("-id").first()
        )

        file_hash = (
            lastest_file_version.hash if lastest_file_version is not None else file.hash
        )
        file_name = file.name

        response = requests.post(
            f"http://{settings.BOOTSTRAP_NODE_HOST}:5001/api/v0/cat?arg={file_hash}"
        )

        if response.status_code == 200:
            file_content = response.content

            file_stream = BytesIO(file_content)

            return FileResponse(file_stream, as_attachment=True, filename=file_name)
        else:
            raise ValidationError(detail={"hash": f"{response.text}."}, code="invalid")
