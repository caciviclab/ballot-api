from rest_framework import serializers
from .models import Candidate, Committee


class CandidateSerializer(serializers.ModelSerializer):
    fppc = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Candidate
        fields = '__all__'


class CommitteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Committee
        fields = '__all__'
