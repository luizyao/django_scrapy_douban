from django.contrib import admin

# Register your models here.
from .models import FilmComments, GradeSummary, PersonSummary

admin.site.register(FilmComments)
admin.site.register(GradeSummary)
admin.site.register(PersonSummary)
