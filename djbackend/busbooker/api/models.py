from typing import Any
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from api.managers import *

class Route(models.Model):
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    distance = models.PositiveIntegerField(default=0)
    
    #managers
    route_manager = RouteManager()
    
    class Meta:
        unique_together = ("source", "destination")

class SeatPlan(models.Model):
    rows = models.PositiveIntegerField(default=2)
    cols = models.PositiveIntegerField(default=2)
    
    @property
    def total_seats(self):
        return (self.rows)*(self.cols)
        
class Bus(models.Model):
    bus_name = models.CharField(max_length=50, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    fare = models.PositiveIntegerField(default=100)

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thrusday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    
    scheduled_date = models.DateField(default=datetime.date(datetime.now()))
    
    route = models.ForeignKey(to = Route, on_delete=models.CASCADE, related_name= "buses", null=True)
    seat_plan = models.OneToOneField(to = SeatPlan, related_name="bus", on_delete=models.SET_NULL, null=True)
    
    bookings = models.ManyToManyField(to = User, through='Booking', related_name='booked_buses')
    
    #managers
    read_only_manager = BusManagerReadOnly()
    
    objects = models.Manager()
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
    def counts_prefetch(self):
        self.update_days_scheduled()
        self.update_total_seats()
        self.update_total_bookings()
        
    @property
    def getDaysScheduled(self):
        if not hasattr(self, "_scheduled_days"): self.counts_prefetch()
        return self._scheduled_days
    
    def update_days_scheduled(self):
        self._scheduled_days = tuple(getattr(self, i) for i in ("monday","tuesday","wednesday","thrusday","friday","saturday","sunday"))
    
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
    