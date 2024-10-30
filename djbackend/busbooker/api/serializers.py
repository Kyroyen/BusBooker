from rest_framework import serializers
from api.models import *


class BusSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()
    total_seats = serializers.SerializerMethodField()
    avaliable_seats = serializers.SerializerMethodField()

    class Meta:
        model = Bus
        fields = [
            "id",
            'bus_name',
            'start_time',
            'end_time',
            'fare',
            "scheduled_date",
            'total_bookings',
            "total_seats",
            "avaliable_seats",
        ]

    def get_total_bookings(self, obj):
        return obj.getTotalBookings

    def get_total_seats(self, obj):
        return obj.getTotalSeats

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
        
