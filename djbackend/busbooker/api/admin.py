from django.contrib import admin
from api.models import *


class BusAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ("bus_name",
                       "start_time",
                       "end_time",
                       "fare",)  # Fields you want outside of the "Schedule" section
        }),
        ('Schedule', {
            'fields': ('monday', 'tuesday', 'wednesday', 'thrusday', 'friday', 'saturday', 'sunday'),
            'classes': ('schedule',),
        }),
        (None, {
            "fields": ("route", "seat_plan")
        })
    )
    class Media:
        css = {
            'all': ('api/admin.css',),  # Replace 'yourapp' with your actual app name
        }


admin.site.register(Route)
admin.site.register(SeatPlan)
admin.site.register(Booking)
admin.site.register(Bus, BusAdmin)
