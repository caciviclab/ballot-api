from rest_framework import serializers
from .models import Candidate


class CandidateSerializer(serializers.ModelSerializer):
    fppc = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Candidate
        fields = '__all__'
