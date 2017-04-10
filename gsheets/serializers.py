from rest_framework import serializers
from .models import Candidate, Committee, Referendum, ReferendumMapping


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


class ReferendumMappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReferendumMapping
        fields = '__all__'
