from rest_framework import permissions


# ======================================================================================================================
# Custom Permission: IsOwnerOrReadOnly
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object to edit it.
    Assumes that the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determines whether the requesting user has permission to access the object.
        """

        # Read permissions are granted to all users.
        # SAFE_METHODS include GET, HEAD, and OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True  # Allow read-only access to any user

        # Write permissions are restricted to the object’s owner.
        # Assumes the model has an 'author' attribute representing ownership.
        return (
            obj.author == request.user
        )  # Allow modification only if the requester is the owner


# ======================================================================================================================
