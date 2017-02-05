from django.core.exceptions import ObjectDoesNotExist

from .models import Candidate
from .serializers import CandidateSerializer


class Parser(object):
    def name(self):
        return self.__class__.model.__name__

    def filter_fields(self, row):
        field_names = self.get_field_names()
        return dict((k, v) for k, v in row.items() if k in field_names)

    def parse(self, row):
        return self.parse_fields(self.filter_fields(row))


class CandidateParser(Parser):
    model = Candidate

    def key(self, row):
        return row.get('candidate', None)

    def exists_in_db(self, row):
        """Determines if this row exists in the database already."""

        name = row.get('candidate', None)
        if not name:
            return False

        exists = True
        try:
            Candidate.objects.get(candidate=name)
        except ObjectDoesNotExist:
            exists = False

        return exists

    def parse_fields(self, row):
        """Parses individual fields in the row that are acceptable to the model."""
        # Convert fppc
        fppc = row.get('fppc', None)
        if not fppc:
            row['fppc'] = None

        # Parse booleans
        accepted_expenditure_ceiling = row.get('accepted_expenditure_ceiling', False)
        row['accepted_expenditure_ceiling'] = bool(accepted_expenditure_ceiling)

        # Convert twitter @handle to URL
        twitter = row.get('twitter', None)
        if twitter:
            # Drop the first char (@)
            row['twitter'] = 'https://twitter.com/%s' % twitter[1:]

        return row

    def get_field_names(self):
        return [field.name for field in Candidate._meta.get_fields()]

    def to_serializer(self, row):
        return CandidateSerializer(data=row)

    def commit(self, serializer):
        return Candidate.objects.update_or_create(candidate=serializer.data.get('candidate'), defaults=serializer.validated_data)
