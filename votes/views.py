from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from guideshareapi.permissions import IsOwnerOrReadOnly
from .models import Vote
from . import serializers


# This class is a generic view that allows us to create a vote
class VoteCreate(generics.CreateAPIView):
    serializer_class = serializers.VoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Vote.objects.all()

    def perform_create(self, serializer):
        """
        It sets the votes owner on creation

        :param serializer: The serializer instance that should be saved
        """
        serializer.save(owner=self.request.user)


# This class will allow users to delete their votes
class VoteDestroy(generics.DestroyAPIView):
    serializer_class = serializers.VoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Vote.objects.all()
