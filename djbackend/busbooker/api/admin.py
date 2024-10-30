from django.contrib import admin
from api.models import *


class BusAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                "bus_name",
                "start_time",
                "end_time",
                "fare",
                "scheduled_date"
            )
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
admin.site.register(RouteStops)
admin.site.register(Stop)
admin.site.register(SeatPlan)
admin.site.register(Booking)
admin.site.register(Bus, BusAdmin)
