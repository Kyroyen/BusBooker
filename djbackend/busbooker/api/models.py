from typing import Any
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from api.managers import *

class Stop(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
    
class Route(models.Model):
    name = models.CharField(max_length=50)
    route_manager = RouteManager()
    
    def __str__(self) -> str:
        return self.name
    
class RouteStops(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="routes")
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name="stops_on_routes")
    stop_sequence = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('route', 'stop', "stop_sequence")
        

class SeatPlan(models.Model):
    name = models.CharField(max_length=50, default="SeatPlan")
    rows = models.PositiveIntegerField(default=2)
    cols = models.PositiveIntegerField(default=2)
    
    def __str__(self) -> str:
        return self.name
    
    @property
    def total_seats(self):
        return (self.rows)*(self.cols)
        
class Bus(models.Model):
    bus_name = models.CharField(max_length=50, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    fare = models.PositiveIntegerField(default=100)
    
    scheduled_date = models.DateField(default=datetime.date(datetime.now()))
    
    route = models.ForeignKey(to = Route, on_delete=models.CASCADE, related_name= "buses", null=True)
    seat_plan = models.ForeignKey(to = SeatPlan, related_name="bus", on_delete=models.SET_NULL, null=True)
    
    bookings = models.ManyToManyField(to = User, through='Booking', related_name='booked_buses')
    
    #managers
    read_only_manager = BusManagerReadOnly()
    
    objects = models.Manager()
    
    def __str__(self) -> str:
        return self.bus_name
        
    def counts_prefetch(self):
        self.update_total_seats()
        self.update_total_bookings()
    
    @property
    def getTotalSeats(self):
        if not hasattr(self, "_total_seats"): self.counts_prefetch()
        return self._total_seats
        
    def update_total_seats(self):
        self._total_seats = self.seat_plan.total_seats if (self.seat_plan is not None) else -1
    
    @property
    def getTotalBookings(self):
        if not hasattr(self, "_total_bookings"): self.counts_prefetch()
        return self._total_bookings
    
    def update_total_bookings(self):
        self._total_bookings = self.bookings.count()
        
    @property
    def getAvailableSeats(self):
        return self.getTotalSeats - self.getTotalBookings


class Booking(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    locked = models.BooleanField(default=True)
    booked = models.BooleanField(default=False)
    
    objects = models.Manager()
    write_manager = BookingsWriteManager()
    read_manager = BookingReadManager()
    
    @property
    def seatNumber(self):
        return f"{self.row}-{self.col}"
    
    class Meta:
        unique_together = ('bus', 'row', 'col')
    