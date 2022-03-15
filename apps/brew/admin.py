from django.contrib import admin
from brew.models import Malt, Hop, Misc, Yeast, BeerStyle, Recipe, MashStep


class MaltAdmin(admin.ModelAdmin):
    list_display = ("name", "potential_gravity", "diastatic_power", "malt_yield")


class YeastAdmin(admin.ModelAdmin):
    list_display = ("name", 'min_attenuation', 'max_attenuation',)


admin.site.register(Malt, MaltAdmin)
admin.site.register(Hop)
admin.site.register(Misc)
admin.site.register(Yeast, YeastAdmin)
admin.site.register(BeerStyle)
admin.site.register(Recipe)
admin.site.register(MashStep)
