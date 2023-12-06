from rest_framework.permissions import BasePermission


class IsCurrentUser(BasePermission):
    def has_permission(self, request, view):
        print(request.user.reader.id)
        return str(request.user.reader.id) == view.kwargs['pk']
