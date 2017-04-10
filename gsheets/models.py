from django.db import models


class CandidateAlias(models.Model):
    """An alternative name for the candidate which may occur in filings."""

    candidate_alias = models.CharField(max_length=30)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, related_name='aliases')

    def __str__(self):
        return self.candidate_alias

    class Meta:
        verbose_name_plural = 'candidate aliases'


class Candidate(models.Model):
    """A person running for office in an election."""

    PARTY_AFFILIATION = [
        ('D', 'Democrat'),
        ('R', 'Republican'),
        ('I', 'Independent'),
        ('O', 'Other'),
    ]

    fppc = models.IntegerField(blank=True, null=True, unique=True)
    committee_name = models.CharField(blank=True, max_length=120)
    candidate = models.CharField(max_length=30, help_text='The candidate\'s full name.')
    office = models.CharField(blank=True, max_length=30, help_text='Office the candidate is running for.')
    incumbent = models.BooleanField(default=False)
    accepted_expenditure_ceiling = models.BooleanField(default=False)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    party_affiliation = models.CharField(blank=True, max_length=1, choices=PARTY_AFFILIATION)
    occupation = models.CharField(blank=True, max_length=80)
    bio = models.TextField(blank=True)
    # TODO use ImageField to support photo uploads
    photo = models.URLField(blank=True, null=True)
    votersedge = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.candidate


class Referendum(models.Model):
    measure_number = models.CharField(max_length=5)
    short_title = models.CharField(blank=True, max_length=200)
    full_title = models.TextField(blank=True)
    summary = models.TextField()
    votersedge = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Referendum %s %s" % (self.measure_number, self.short_title)


class Committee(models.Model):
    COMMITTEE_TYPES = [
        ('RCP', 'RCP'),
        ('BMC', 'BMC'),
    ]

    SUPPORT_OPPOSE = [
        ('S', 'Support'),
        ('O', 'Oppose'),
    ]

    filer_id = models.CharField(max_length=15)
    filer_naml = models.CharField(blank=True, max_length=200)
    committee_type = models.CharField(blank=True, max_length=3, choices=COMMITTEE_TYPES)
    description = models.CharField(blank=True, max_length=40)
    ballot_measure = models.CharField(blank=True, max_length=3)
    support_or_oppose = models.CharField(blank=True, max_length=1, choices=SUPPORT_OPPOSE)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    netfilelocalid = models.CharField(blank=True, max_length=15)

    def __str__(self):
        return self.filer_naml


class ReferendumMapping(models.Model):
    measure_name = models.CharField(max_length=200)
    measure_number = models.CharField(max_length=10)

    def __str__(self):
        return '%s: %s' % (self.measure_number, self.measure_name)
