from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from guideshareapi.permissions import IsOwnerOrReadOnly
from .models import Vote
from . import serializers


class VoteCreate(generics.CreateAPIView):
    serializer_class = serializers.VoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Vote.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class VoteDestroy(generics.DestroyAPIView):
    serializer_class = serializers.VoteSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Vote.objects.all()
