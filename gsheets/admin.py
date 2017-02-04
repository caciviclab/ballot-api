from django.contrib import admin

from .models import Candidate, Committee, Referendum, ReferendumMapping

admin.site.register(Candidate)
admin.site.register(Referendum)
admin.site.register(ReferendumMapping)
admin.site.register(Committee)
