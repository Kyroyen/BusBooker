from django.contrib import admin
from api.models import *

from django.contrib import admin

admin.site.site_title = "Bus Manager Admin"
admin.site.site_header = "Bus Manager Admin Portal"
admin.site.index_title = "Welcome to My Bus System Admin Dashboard"

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
            'all': ('api/admin.css',),
        }

class RouteStopInline(admin.TabularInline):
    model = RouteStops
    extra = 3
    min_num = 1
    fields = ('stop', 'stop_sequence', "travel_time")

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    inlines = [RouteStopInline]
    list_display = ('name',)
    
admin.site.register(Stop)
admin.site.register(SeatPlan)
admin.site.register(Booking)
admin.site.register(Bus, BusAdmin)
