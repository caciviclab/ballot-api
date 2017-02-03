from rest_framework import viewsets
from .models import Candidate, Election
from .serializers import CandidateSerializer, ElectionSerializer


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Candidates to be viewed.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Elections to be viewed.
    """
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
