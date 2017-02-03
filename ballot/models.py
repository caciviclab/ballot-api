
from django.db import models


class Filer(models.Model):
    """Not from Voter Information Project. A filer in the state of
    California."""

    filer_id = models.CharField(max_length=20, null=False)
    name = models.TextField()


class State(models.Model):
    """The State object includes state-wide election information. The ID
    attribute is recommended to be the state’s FIPS code, along with the prefix
    “st”."""

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name or 'Unknown'


class Person(models.Model):
    """Person defines information about a person. The person may be a
    candidate, election administrator, or elected official. These elements
    reference Person:

    - Candidate
    - ElectionAdministration
    - Office
    """

    first_name = models.CharField(blank=True, max_length=30)
    full_name = models.CharField(max_length=60)
    last_name = models.CharField(blank=True, max_length=30)
    middle_name = models.CharField(blank=True, max_length=30)

    # non-vip fields
    biography = models.TextField(blank=True)
    filer = models.ForeignKey('Filer', null=True)
    occupation = models.CharField(blank=True, max_length=30)
    party_affiliation = models.CharField(blank=True, max_length=20)
    photo = models.ImageField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    voters_edge_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'people'


class Candidate(models.Model):
    """The Candidate object represents a candidate in a contest. If a candidate
    is running in multiple contests, each contest must have its own Candidate
    object. Candidate objects may not be reused between Contests."""

    ballot_name = models.CharField(max_length=128, blank=False, null=False)
    file_date = models.DateField()
    is_incumbent = models.BooleanField()
    person = models.ForeignKey('Person')


DEFAULT_STATE_ID = 1


class Election(models.Model):
    """The Election object represents an Election Day, which usually consists
    of many individual contests and/or referenda. A feed must contain exactly
    one Election object. All relationships in the feed (e.g., street segment to
    precinct to polling location) are assumed to relate only to the Election
    specified by this object. It is permissible, and recommended, to combine
    unrelated contests (e.g., a special election and a general election) that
    occur on the same day into one feed with one Election object."""

    ELECTION_TYPES = [
        ('F', 'Federal'),
        ('S', 'State'),
        ('CO', 'County'),
        ('C', 'City'),
    ]

    date = models.DateField(unique=True)
    election_type = models.CharField(max_length=2, choices=ELECTION_TYPES)
    is_statewide = models.BooleanField()
    name = models.TextField(blank=True)
    results_uri = models.URLField(blank=True)
    state = models.ForeignKey('State', default=1)

    def __str__(self):
        return self.name or '%s %s Election' % (self.get_election_type_display(), self.date.strftime('%B %-d, %Y'))
