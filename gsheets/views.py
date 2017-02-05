from rest_framework import viewsets
from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Candidates to be viewed.
    """
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
