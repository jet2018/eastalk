from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    message = "You need to be an author to perform this action"
    """
    Object-level permission to only allow authors to add articles.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.profile.is_author:
            return True

        return False
