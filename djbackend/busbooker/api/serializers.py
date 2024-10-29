from rest_framework import serializers
from api.models import *


class BusSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()
    total_seats = serializers.SerializerMethodField()
    days_scheduled = serializers.SerializerMethodField()
    avaliable_seats = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = [
            "id",
            'bus_name',
            'start_time',
            'end_time',
            'fare',
            'total_bookings',
            "total_seats",
            "days_scheduled",
            "avaliable_seats",
        ]

    def get_total_bookings(self, obj):
        return obj.getTotalBookings

    def get_total_seats(self, obj):
        return obj.getTotalSeats

    def get_days_scheduled(self, obj):
        return obj.getDaysScheduled

    def get_avaliable_seats(self, obj):
        return obj.getAvailableSeats
    
class BookedBusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = [
            "id",
            'bus_name',
            'fare'
        ]
        
