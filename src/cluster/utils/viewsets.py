from django.db.models import ProtectedError
from rest_framework import status, viewsets
from rest_framework.response import Response
from utils.errors import AssociatedError


class ProtectedDeleteViewSet(viewsets.ModelViewSet):
    """
    A ModelViewSet subclass that overrides the `destroy` method to handle cases
    where an object cannot be deleted due to a `ProtectedError`.

    This viewset catches `ProtectedError` exceptions, which occur when attempting to
    delete an object that is protected by foreign key relationships with
    `on_delete=PROTECT`. Instead of returning the default behavior, it raises a custom
    `AssociatedError`.

    Methods:
        destroy(request, *args, **kwargs):
            Tries to delete an object. If successful, returns a 204 No Content response.
            If the object is protected by related models, raises an `AssociatedError`.

    Args:
        request: The HTTP request object.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Raises:
        AssociatedError: If the object cannot be deleted due to related models using
        `on_delete=PROTECT`.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            raise AssociatedError()
