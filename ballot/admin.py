from django.contrib import admin

from .models import Candidate
from .models import Election
from .models import Person
from .models import State


class CandidateInline(admin.StackedInline):
    model = Candidate


class PersonAdmin(admin.ModelAdmin):
    exclude = ('filer',)


class BallotApiAdminSite(admin.AdminSite):
    site_header = 'Open Disclosure Ballot API Admin'


api_admin = BallotApiAdminSite(name='ballotapi-admin')
api_admin.register(Election)
api_admin.register(Person, PersonAdmin)
api_admin.register(State)
