from django.core.exceptions import ObjectDoesNotExist

from .models import Candidate, Committee, Referendum, ReferendumMapping
from .serializers import CandidateSerializer, CommitteeSerializer, ReferendumSerializer, ReferendumMappingSerializer


class Parser(object):
    @property
    def name(self):
        return self.model.__name__

    def filter_fields(self, row):
        field_names = self.get_field_names()
        return dict((k, v) for k, v in row.items() if k in field_names)

    def parse(self, row):
        return self.parse_fields(self.filter_fields(row))

    def parse_fields(self, row):
        """Subclasses should override this method to transform the row to appropriate types"""

        return row

    def get_field_names(self):
        return [field.name for field in self.model._meta.get_fields()]

    def exists_in_db(self, row):
        """Determines if this row exists in the database already."""

        id = row.get(self.key, None)
        if not id:
            return False

        kwargs = {self.key: id}
        exists = True
        try:
            self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            exists = False

        return exists

    def to_serializer(self, row):
        return self.__class__.serializer(data=row)

    def commit(self, serializer):
        id = serializer.data.get(self.key)
        kwargs = {
            self.key: id,
            "defaults": serializer.validated_data
        }

        return self.model.objects.update_or_create(**kwargs)


class CandidateParser(Parser):
    model = Candidate
    key = 'candidate'
    serializer = CandidateSerializer

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


class CommitteeParser(Parser):
    model = Committee
    key = 'filer_id'
    serializer = CommitteeSerializer

    def parse_fields(self, row):
        twitter = row.get('twitter', None)
        if twitter:
            # Drop the first char (@)
            twitter = 'https://twitter.com/%s' % twitter[1:]

        parsed = dict(row)
        parsed.update(
            twitter=twitter,
        )

        return parsed


class ReferendumParser(Parser):
    model = Referendum
    key = 'measure_number'
    serializer = ReferendumSerializer


class ReferendumMappingParser(Parser):
    model = ReferendumMapping
    key = 'measure_number'
    serializer = ReferendumMappingSerializer
