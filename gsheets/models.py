from django.db import models


class Candidate(models.Model):
    fppc = models.IntegerField(blank=True, null=True, unique=True)
    committee_name = models.CharField(max_length=60)
    candidate = models.CharField(max_length=30)
    aliases = models.TextField(
            blank=True,
            help_text='Comma separated list of alternative spellings and names within the filings.')
    office = models.CharField(blank=True, max_length=30, help_text='Office the candidate is running for.')
    incumbent = models.BooleanField()
    accepted_expenditure_ceiling = models.BooleanField()
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    party_affiliation = models.CharField(blank=True, max_length=15)
    occupation = models.CharField(blank=True, max_length=30)
    bio = models.TextField(blank=True)
    photo = models.ImageField(blank=True, null=True)
    votersedge = models.URLField(blank=True, null=True)


class Referendum(models.Model):
    measure_number = models.CharField(max_length=5)
    short_title = models.CharField(blank=True, max_length=30)
    full_title = models.TextField(blank=True)
    summary = models.TextField()
    votersedge = models.URLField(blank=True, null=True)


class Committee(models.Model):
    COMMITTEE_TYPES = [
        ('RCP', 'RCP'),
        ('BMC', 'BMC'),
    ]

    SUPPORT_OPPOSE = [
        ('S', 'Support'),
        ('O', 'Oppose'),
    ]

    filer_id = models.IntegerField()
    filer_naml = models.CharField(blank=True, max_length=20)
    committee_type = models.CharField(blank=True, max_length=3, choices=COMMITTEE_TYPES)
    description = models.CharField(blank=True, max_length=20)
    ballot_measure = models.CharField(blank=True, max_length=3)
    support_or_oppose = models.CharField(blank=True, max_length=1, choices=SUPPORT_OPPOSE)
    website = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    netfilelocalid = models.CharField(blank=True, max_length=15)


class ReferendumMapping(models.Model):
    measure_name = models.CharField(max_length=30)
    measure_number = models.CharField(max_length=3)
