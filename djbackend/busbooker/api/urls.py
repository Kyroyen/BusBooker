from django.urls import path
from api.views import *

urlpatterns = [
    path("routes", RouteBuses.as_view(), name="bus-routes"),
    path("bus/<int:bus_id>", BusView.as_view(), name="buses"),
    path("booking/",  BookingView.as_view(), name="bookings"),
    path("token/", CustomTokenAuthentication.as_view(), name="token-auth"),
]
