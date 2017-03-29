from django.core.exceptions import ObjectDoesNotExist

from .models import Candidate, CandidateAlias, Committee, Referendum, ReferendumMapping
from .serializers import CandidateSerializer, CommitteeSerializer, ReferendumSerializer, ReferendumMappingSerializer


def get_or_none(key, row):
    value = row.get(key, None)
    # Convert falsy values to None
    if not value:
        value = None

    return value


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

    def commit(self, data):
        id = data.get(self.key)
        kwargs = {
            self.key: id,
            "defaults": data
        }

        return self.model.objects.update_or_create(**kwargs)


class CandidateParser(Parser):
    model = Candidate
    key = 'candidate'
    serializer = CandidateSerializer

    def parse_party_affiliation(self, row):
        party_affiliation = row.get('party_affiliation', None)
        if not party_affiliation:
            return 'O'

        # Take only the first character
        party_affiliation = party_affiliation[0]
        if party_affiliation not in [k for k, _ in Candidate.PARTY_AFFILIATION]:
            return 'O'

        return party_affiliation

    def parse(self, row):
        """Parses individual fields in the row that are acceptable to the model."""

        data = self.filter_fields(row)

        # We'll handle aliases below, don't pass them to the eventual model
        del data['aliases']

        # Convert empty strings to None
        fppc = get_or_none('fppc', row)

        # Convert empty strings to bool
        accepted_expenditure_ceiling = bool(row.get('accepted_expenditure_ceiling', False))

        # Party affiliation
        party_affiliation = self.parse_party_affiliation(row)

        # Convert twitter @handle to URL
        twitter = row.get('twitter', None)
        if twitter:
            # Drop the first char (@)
            twitter = 'https://twitter.com/%s' % twitter[1:]

        data.update(
            fppc=fppc,
            accepted_expenditure_ceiling=accepted_expenditure_ceiling,
            party_affiliation=party_affiliation,
            twitter=twitter)

        candidate, created = self.commit(data)

        # Parse aliases
        alias_parser = CandidateAliasParser()
        candidate_aliases = row.get('aliases', '').split(',')
        for candidate_alias in candidate_aliases:
            if not candidate_alias:
                continue

            alias = alias_parser.parse(dict(candidate_alias=candidate_alias, candidate=candidate))
            alias_parser.commit(alias)

        return data


class CandidateAliasParser(Parser):
    model = CandidateAlias
    key = 'candidate_alias'

    def parse(self, row):
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
