from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from .models import CustomUser, Poll, Choice, Vote
from .serializer import UserSerializer, PollSerializer, ChoiceSerializer, VoteSerializer


class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class PollCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PollSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PollListView(ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ChoiceCreateView(CreateAPIView):
    serializer_class = ChoiceSerializer

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('pk')
        poll_obj = get_object_or_404(Poll, id=poll_id)
        serializer.save(poll_obj=poll_obj)


class VoteCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        poll_id = self.kwargs.get('pk')
        poll_object = get_object_or_404(Poll, id=poll_id)

        valid_choice_objects = Choice.objects.filter(
            poll_obj=poll_object
        )

        choice_object = serializer.validated_data.get('choice_obj')

        if not valid_choice_objects.filter(
            id=choice_object.id
        ).exists():
            raise serializers.ValidationError(
                {
                    "choice_obj": "This choice does not belong to this poll."
                }
            )

        serializer.save(
            poll_obj=poll_object,
            owner_obj=self.request.user
        )


class PollDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer