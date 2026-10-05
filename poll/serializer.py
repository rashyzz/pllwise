from rest_framework import serializers
from poll.models import CustomUser, Poll, Choice, Vote


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'phone']
        read_only_fields = ['id']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class ChoiceSerializer(serializers.ModelSerializer):
    votes=serializers.SerializerMethodField()
    voters=serializers.SerializerMethodField()
    class Meta:
        model = Choice
        fields = '__all__'
        read_only_fields = ['id', 'poll_obj']
    def get_votes(self,objects):
        votes_qs=Vote.objects.filter(choice_obj=objects)
        return votes_qs.count()
    def get_voters(self,object):
        votes_qs=Vote.objects.filter(choice_obj=object)
        return votes_qs.values_list('owner_obj__username',flat=True)
    


class PollSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    choices = serializers.SerializerMethodField()
    total_vote = serializers.SerializerMethodField()

    class Meta:
        model = Poll
        fields = '__all__'
        read_only_fields = [
            'id',
            'owner',
            'created_at',
            'is_active'
        ]

    def get_choices(self, obj):
        choice_qs = Choice.objects.filter(poll_obj=obj)
        serializer = ChoiceSerializer(choice_qs, many=True)
        return serializer.data

    def get_total_vote(self, obj):
        votes_qs = Vote.objects.filter(poll_obj=obj)
        return votes_qs.count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
        read_only_fields = [
            'id',
            'poll_obj',
            'owner_obj',
            'created_at'
        ]