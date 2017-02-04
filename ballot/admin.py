from django.contrib import admin

from .models import Candidate
from .models import Election
from .models import Person
from .models import State


class CandidateInline(admin.StackedInline):
    model = Candidate


class PersonAdmin(admin.ModelAdmin):
    exclude = ('filer',)


admin.site.site_header = 'Open Disclosure Ballot API Admin'
admin.site.register(Election)
admin.site.register(Person, PersonAdmin)
admin.site.register(State)
