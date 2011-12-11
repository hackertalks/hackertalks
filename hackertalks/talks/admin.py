from django.contrib import admin
from models import Talk, TalkFeature

def refresh_from_blip(modeladmin, request, queryset):
    for x in queryset:
        x.refresh_from_blip()

class TalkAdmin(admin.ModelAdmin):
    actions = [refresh_from_blip]

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkFeature)
