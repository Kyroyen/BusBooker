from django.db.models.manager import Manager
from django.db import transaction, connection
from django.core.cache import cache
from django.db.models import Sum

from typing import List, Tuple


class SeatArrangementMaker:

    @classmethod
    def intoInteger(cls, rows, cols):
        return rows*1000 + cols

    @classmethod
    def intoRowsCols(cls, rows_cols):
        return divmod(rows_cols, 1000)


class RouteManager(Manager):

    def get_ETA_to_seq(self, route_id, sequence_ind):
        cache_key = f"Buses_traveltime_in_route_seqind:{route_id};{sequence_ind}"
        total_travel_time = cache.get(cache_key)
        if total_travel_time is None:
            total_travel_time = self.get_queryset().get(
                id=route_id
            ).routes.filter(stop_sequence__lte=sequence_ind).aggregate(Sum('travel_time'))['travel_time__sum']
            cache.set(cache_key, total_travel_time, 60)

        return total_travel_time

    def get_routes_ids_in_stops(self, start_stop_id, end_stop_id):
        cache_key = f"Buses_in_stops:{start_stop_id};{end_stop_id}"
        route_ids = cache.get(cache_key)
        if route_ids is None:
            query = '''
                SELECT DISTINCT r1.route_id 
                FROM api_routestops as r1 JOIN api_routestops 
                as r2 ON r1.route_id=r2.route_id
                WHERE r1.stop_id=%s and r2.stop_id=%s 
                and r1.stop_sequence<r2.stop_sequence;
                '''
            with connection.cursor() as cursor:
                cursor.execute(
                    query, (start_stop_id, end_stop_id)
                )
                route_ids = [row[0] for row in cursor.fetchall()]
            cache.set(cache_key, route_ids, timeout=200)
        return route_ids

    def get_bus_in_routes(self, start_stop_id, end_stop_id):
        route_id = self.get_routes_ids_in_stops(start_stop_id, end_stop_id)
        return route_id
    
class RouteStopReadManager(Manager):
    
    def get_sequence_id_from_route_stop(self, route_id, stop_id):
        cache_key = f"route_stop_to_sequence_ind:{route_id};{stop_id}"
        sequence_id = cache.get(cache_key)
        if sequence_id is None:
            sequence_id = self.get_queryset().filter(route__id = route_id, stop__id = stop_id).first().stop_sequence
        return sequence_id


class BusManagerBase(Manager):

    def get_querybase(self):
        return self.get_queryset()

    def get_bus(self, bus_id):
        return self.get_querybase().filter(id=bus_id).first()


class BusManagerReadOnly(BusManagerBase):

    def get_bus(self, bus_id, initialze_counts: bool = False):
        cache_key = f"bus_data:{bus_id}"

        bus = cache.get(cache_key)

        if bus is None:
            bus = super().get_bus(bus_id)
            if bus is None:
                return None
            if initialze_counts:
                bus.counts_prefetch()
            cache.set(cache_key, bus, 60)

        return bus

    def get_busid_list_from_routeid_list(self, route_ids_list):
        print(route_ids_list)
        ert = self.get_querybase().filter(route__id__in=route_ids_list).values_list('id', "route__id")
        if not ert:
            return [[],[]]
        return zip(*ert)

    def get_buses_from_flat_list(self, busid_flat_list):
        return [self.get_bus(id) for id in busid_flat_list]

    def get_seatarrangement(self, bus_id):
        cache_key = f"bus_seat_grid_data:{bus_id}"
        bus_seat_data = cache.get(cache_key)

        if bus_seat_data is None:
            bus = self.get_bus(bus_id)
            if bus is None:
                return None
            bookings = bus.booking_set.all()
            bus_seat_data = tuple(SeatArrangementMaker.intoInteger(
                i.row, i.col) for i in bookings)
            cache.set(cache_key, bus_seat_data, 60)

        return bus_seat_data


class BookingManager(Manager):

    def get_querybase(self):
        return self.get_queryset()

    def get_locked_query(self):
        return self.get_querybase().filter(locked=True)

    def get_booked_query(self):
        return self.get_querybase().filter(booked=True)

    def check_if_lock_possible(self, seats: List[Tuple[int, int]], bus, user):
        return not any(self.get_querybase().filter(bus=bus, row=row, col=col).exists() for row, col in seats)


class BookingsWriteManager(BookingManager):

    def lock_seats(self, bus, user, seats: List[tuple[int, int]]):

        if not self.check_if_lock_possible(seats, bus, user):
            return False

        bookings_to_create = []

        for row, col in seats:
            bookings_to_create.append(
                self.model(bus=bus, user=user, row=row, col=col)
            )

        try:
            with transaction.atomic():
                self.bulk_create(bookings_to_create)
            cache.delete_many([f"bus_seat_grid_data:{bus.id}", f"bus_seat_data:{
                              bus.id}", f"bus_data:{bus.id}"])
            return True
        except:
            return False

    def confirm_seats(self, bus, user):

        queryset = self.get_queryset().filter(
            bus=bus, user=user, locked=True, booked=False)
        if not queryset:
            return False
        if self.get_queryset().filter(bus=bus, user=user, locked=True).exists():
            cache.delete_many([f"bus_seat_grid_data:{bus.id}", f"bus_seat_data:{bus.id}", f"bus_data:{bus.id}"])
            queryset.update(booked=True)
            return True

    def booking_cancel(self, bus, user):
        queryset = self.get_queryset().filter(bus=bus, user=user, locked=True)
        if not queryset:
            return False
        if queryset.delete():
            cache.delete_many([f"bus_seat_grid_data:{bus.id}", f"bus_seat_data:{
                              bus.id}", f"bus_data:{bus.id}"])
            return True
        return False


class BookingReadManager(BookingManager):

    def get_user_booked_buses(self, user):
        bus_ids = self.get_booked_query().filter(
            user=user).values_list('bus', flat=True).distinct()
        return bus_ids

    def get_counts_for_user_in_bus(self, bus_id, user):
        return self.get_booked_query().filter(user=user, bus__id=bus_id, booked=True).values("row", "col", "bus__id")
