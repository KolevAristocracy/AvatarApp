from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from profile_api.serializers import ProfileSerializer


class UserProfileAPIView(RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile