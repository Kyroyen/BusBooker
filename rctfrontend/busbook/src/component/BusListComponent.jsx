import { useState, useEffect } from "react";

function BusListComponent({ busData, onClick }) {
  const percentageFill = (busData.avaliable_seats / busData.total_seats) * 100;
  

  const getBackgroundColor = (occupancy) => {
    if (occupancy <= 60) {
        return 'bg-red-200'; // Light red for 90% to 100%
    } else if (occupancy > 60 && occupancy < 90) {
        return 'bg-yellow-200'; // Light yellow for 60% to 90%
    } else {
        return 'bg-green-200'; // Light green for 60% or less
    }
  };
  
  const getBorderColor = (occupancy) => {
    if (occupancy <= 60) {
        return 'border-red-500'; // Dark red for 90% to 100%
    } else if (occupancy > 60 && occupancy < 90) {
        return 'border-yellow-500'; // Dark yellow for 60% to 90%
    } else {
        return 'border-green-500'; // Dark green for 60% or less
    }
  };

  
  const backgroundColor = getBackgroundColor(percentageFill);
  const borderColor = getBorderColor(percentageFill);


  return (
    <div onClick={(e) => onClick(busData)} className={`w-full rounded-lg p-4 mb-4 flex flex-row space-x-5 justify-between border-x-8 border-y-2 ${backgroundColor} ${borderColor} cursor-pointer`}>
      <span>{busData.id}</span>
      <span>{busData.bus_name}</span>
      <span>{busData.end_time}</span>
      <span>{busData.start_time}</span>
      <span>{busData.fare}</span>
      <span>{busData.scheduled_date	}</span>
      <span>{busData.avaliable_seats}</span>
    </div>
  );
}

export default BusListComponent;
