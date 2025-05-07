from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([User, Season, Track, Driver, Type_of_race, Race, Starting_grid, Rating])
