from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.UserProfile)

admin.site.register(models.Movie)
admin.site.register(models.TVShow)
admin.site.register(models.Rating)
admin.site.register(models.Genre)