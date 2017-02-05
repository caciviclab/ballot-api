from rest_framework import serializers
from .models import Candidate, Committee, Referendum


class CandidateSerializer(serializers.ModelSerializer):
    fppc = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Candidate
        fields = '__all__'


class CommitteeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Committee
        fields = '__all__'


class ReferendumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referendum
        fields = '__all__'
