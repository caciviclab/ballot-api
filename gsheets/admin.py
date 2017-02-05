from django.contrib import admin

from .models import Candidate, CandidateAlias, Committee, Referendum, ReferendumMapping


class CandidateAliasInline(admin.TabularInline):
    model = CandidateAlias


class CandidateAdmin(admin.ModelAdmin):
    inlines = (CandidateAliasInline,)


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateAlias)
admin.site.register(Referendum)
admin.site.register(ReferendumMapping)
admin.site.register(Committee)
