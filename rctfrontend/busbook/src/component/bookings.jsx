import { useEffect, useState } from "react";
import axiosInstance from "../api/axiosInstance.js";

function BookingsPage() {
  const [bookedData, setBookedData] = useState([]);

  const fetchBookedItems = async () => {
    try {
      const response = await axiosInstance.get("/booking/");

      setBookedData(response.data);
      console.log("resp", response.data);
    } catch (error) {
      console.error("Error fetching booked items", error);
    }
  };

  const handleCancelBooking = async (bus_id) => {
    console.log("cancel booking", bus_id);
    await axiosInstance.delete("/booking/", {
      data: { bus_id: bus_id }
    })
    .finally(async () => {
      await fetchBookedItems();
    })
    .catch(async () => {
      await fetchBookedItems();
    }
    );
    
  }

  useEffect(() => {
    fetchBookedItems();
  }, []);

  function BookedBusListComponent({ busData }) {
    return (
      <>
        <div
          className={`w-full rounded-lg p-4 mb-4 flex flex-col space-y-0 justify-between bg-yellow-50 border-yellow-600 border`}
        >
          <div className="w-full justify-between p-4 mb-4 flex flex-row space-x-5">
            <span>{busData.id}</span>
            <span>{busData.bus_data.bus_name}</span>
            <span>{busData.bus_data.fare * busData.seats.length}</span>
            <span>{busData.bus_data.scheduled_date}</span>
            <span>{busData.bus_data.start_time}</span>
            <span>{busData.bus_data.end_time}</span>
          </div>
          <div className="w-full justify-between flex flex-row space-x-5 px-4">
            <div className="w-full justify-between px-4 mb-4 space-x-5">
              <span>SEATS: </span>
              {busData.seats.map((item, ind) => {
                return (
                  <span key={ind} className="bg-amber-400 px-2 py-1 rounded-md">
                    <strong>{item}</strong>
                  </span>
                );
              })}
            </div>
            <button onClick={(e) => {handleCancelBooking(busData.id)}} className="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900">
              Cancel
            </button>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <div>
        <div className="flex items-center justify-center space-x-2 py-10">
          <h1 className=" font-bold ">Your Bookings</h1>
        </div>
        <div>
          <div className="w-full justify-center flex">
            <div className="w-[70%] flex flex-col items-center justify-center space-y-2 py-5 ">
              <div className="w-full rounded-lg px-5 mb-4 flex flex-row space-x-5 justify-between">
                <span>BusID</span>
                <span>Name</span>
                <span>Cost</span>
                <span>Date</span>
                <span>Start Time</span>
                <span>End Time</span>
              </div>

              {bookedData.map((item) => {
                return <BookedBusListComponent key={item.id} busData={item} />;
              })}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default BookingsPage;
