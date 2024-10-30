from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.cache import cache

from api.models import *
from api.serializers import *
from api.CustomAuthentication import CustomAuthentication


class CustomTokenAuthentication(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if (username is None) or (password is None):
            return Response(data={"message": "Include both things in request"}, status=403)

        user = User.objects.get(username=username)
        if user.check_password(password):
            return Response(
                data={
                    "message": "Authentication successful",
                    'access_token': CustomAuthentication().create_auth_token(user),
                    'refresh_token': CustomAuthentication().create_auth_token(user, 60*60*24)
                },
                status=200
            )
        return Response(data={"error": "Can't create token"}, status=200)
    
    def put(self, request):
        token = request.data.get("token")
        try:
            user = CustomAuthentication().check_auth_token(token)
            return Response(
                data={
                    "message": "Authentication successful",
                    'token': CustomAuthentication().create_auth_token(user)
                },
                status=200
            )
        except Exception:
            return Response(data={"error": "Can't create token"}, status=200)

class RouteBuses(APIView):

    def get(self, request):
        #cache
        start = request.GET.get("start")
        end = request.GET.get("end")
        cache_key = f"bus_route:{start};{end}"
        data = cache.get(cache_key)
        
        if data is None:
            try:
                start_stop_id = Stop.objects.get(name = start).id
                stop_stop_id = Stop.objects.get(name = end).id
            except Stop.DoesNotExist:
                return Response(data={"message": "Nothing to show"}, status=404)
            
            routes_between_stops = Route.route_manager.get_bus_in_routes(
                start_stop_id= start_stop_id, end_stop_id=stop_stop_id
                )
            
            buses_between_stops = Bus.read_only_manager.get_busid_list_from_routeid_list(
                routes_between_stops
            )

            serializer = BusSerializer(
                Bus.read_only_manager.get_buses_from_flat_list(buses_between_stops), 
                many=True
            )
            data = serializer.data
            cache.set(cache_key,  data, 60)

        return Response(data)


class BusView(APIView):

    def get(self, request, bus_id):
        cache_key = f"bus_data:{bus_id}"
        bus_data = cache.get(cache_key)

        if bus_data is None:
            bus = Bus.read_only_manager.get_bus(bus_id, initialze_counts = True)
            if bus is None:
                return Response(data={"message": "Nothing to show"}, status=404)
            bus_data = BusSerializer(bus).data
            cache.set(cache_key, bus_data, 60)
            
        return Response(data=bus_data, status=200)

    def post(self, request, bus_id):
        
        cache_key = f"bus_seat_data:{bus_id}"
        bus_seat_data = cache.get(cache_key)

        if bus_seat_data is None:
            bus = Bus.read_only_manager.get_seatarrangement(bus_id)
            if bus is None:
                return Response(data={"message": "Nothing to show"}, status=404)
            busobj = Bus.objects.get(pk=bus_id).seat_plan

            bus_seat_data = {
                "occupied": bus,
                "wide": 10 if busobj is None else busobj.rows,
                "long": 10 if busobj is None else busobj.cols,
            }
            cache.set(cache_key, bus_seat_data, 30)
            
        return Response(data=bus_seat_data, status=200)


class BookingView(APIView):

    def get(self, request):
        try:
            user = CustomAuthentication().authenticate(request)
        except:
            return Response(data={"error": "Can't authenticate"}, status=403)
        
        booked_buses = Booking.read_manager.get_user_booked_buses(user)
        booking_data = [
            {
                "id": bus_id,
                "bus_data": (BusSerializer(Bus.read_only_manager.get_bus(bus_id, initialze_counts = True)).data),
            }
            for bus_id in booked_buses
        ]
        for booking in booking_data:
            seats_in_booking = Booking.read_manager.get_counts_for_user_in_bus(
                booking["id"], user
            )
            booking["seats"] = [SeatArrangementMaker.intoInteger(
                i["row"], i["col"]) for i in seats_in_booking]
        return Response(data=booking_data, status=200)

    def post(self, request):
        try:
            user = CustomAuthentication().authenticate(request)
        except:
            return Response(data={"error": "Can't authenticate"}, status=403)
        
        bus_id = request.data.get("bus_id")
        try:
            bus = Bus.objects.get(pk=bus_id)
        except Bus.DoesNotExist:
            return Response(data={"error": "Bus not found"}, status=404)
        encoded_seats = request.data.get("seats", [])
        seats = [
            SeatArrangementMaker.intoRowsCols(seat)
            for seat in encoded_seats
            ]
        print(user, encoded_seats, seats)
        if Booking.write_manager.lock_seats(bus, user, seats):
            return Response(data={"message": "Seat Availability Confirmed"}, status=301)
        else:
            return Response(data={"message": "Some Error Occured, Try Again"}, status=405)

    def put(self, request):
        try:
            user = CustomAuthentication().authenticate(request)
        except:
            return Response(data={"error": "Can't authenticate"}, status=403)
        bus_id = request.data.get("bus_id")
        try:
            bus = Bus.objects.get(pk=bus_id)
        except Bus.DoesNotExist:
            return Response(data={"error": "Bus not found"}, status=404)
        if Booking.write_manager.confirm_seats(bus, user):
            return Response(data={"message": "Seats Booked"}, status=301)
        else:
            return Response(data={"message": "Some Error Occured"}, status=405)

    def delete(self, request):
        try:
            user = CustomAuthentication().authenticate(request)
        except:
            return Response(data={"error": "Can't authenticate"}, status=403)
        bus_id = request.data.get("bus_id")
        try:
            bus = Bus.objects.get(pk=bus_id)
        except Bus.DoesNotExist:
            return Response(data={"error": "Bus not found"}, status=404)
        if Booking.write_manager.booking_cancel(bus, user):
            return Response(data={"message": "Seats cancelled!"}, status=301)
        else:
            return Response(data={"message": "Some Error Occured"}, status=405)
