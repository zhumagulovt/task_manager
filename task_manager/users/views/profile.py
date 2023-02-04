from rest_framework.generics import RetrieveUpdateDestroyAPIView

from rest_framework.permissions import IsAuthenticated

from ..serializers import UserSerializer


class ProfileAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user
