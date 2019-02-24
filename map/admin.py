from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import *
# Register your models here.

admin.site.register(gym, LeafletGeoAdmin)
admin.site.register(pokemon)
admin.site.register(research)
admin.site.register(raid)
admin.site.register(raid_ing)
admin.site.register(event)