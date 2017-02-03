from rest_framework import serializers
from .models import Candidate, Election


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Candidate
        depth = 1


class ElectionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Election
