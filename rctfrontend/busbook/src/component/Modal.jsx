import { useState, useEffect } from "react";
import React from "react";
import axiosInstance from "../api/axiosInstance";
import { useNavigate } from "react-router-dom";

function Modal({ busData, onClose }) {
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [nonAvaliableSeats, setNonAvailableSeats] = useState([]);
  const [rows, setRows] = useState(5);
  const [cols, setCols] = useState(5);
  const [showConfirm, setShowConfirm] = useState(false);
  const navigate = useNavigate();
  const bus_id = busData.id;

  const handleGetBusSeatData = async (bus_id) => {
    await axiosInstance
      .post(`/bus/${bus_id}`)
      .then((value) => {
        setRows(value.data.wide);
        setCols(value.data.long);
        setNonAvailableSeats(value.data.occupied);
      })
      .catch((e) => {
        console.log(e);
      });
  };

  useEffect(() => {
    console.log("Update Bus seatData");
    handleGetBusSeatData(bus_id);
  }, []);

  const lockSeats = async () => {
    const seats = selectedSeats.map((value) => {
      return value.row * 1000 + value.col;
    });
    await axiosInstance
      .post("/booking/", {
        bus_id: bus_id,
        seats: seats,
      })
      .then(() => {
        setShowConfirm(true);
      })
      .catch(() => {
        console.log("show error");
      });
  };

  const bookSeats = async () => {
    await axiosInstance
      .put("/booking/", {
        bus_id: bus_id,
      })
      .then(() => {
        setShowConfirm(false);
        handleGetBusSeatData(bus_id);
        navigate("/bookings");
      })
      .catch(() => {
        console.log("show error");
      });
  };

  const cancelSeats = async () => {
    await axiosInstance
      .delete("/booking/", {
        data: { bus_id: bus_id },
      })
      .then(() => {
        setShowConfirm(false);
        handleGetBusSeatData(bus_id);
      })
      .catch(() => {
        console.log("show error");
      });
  };

  const toggleSeatSelection = (row, col) => {
    const seatIndex = selectedSeats.findIndex(
      (seat) => seat.row === row && seat.col === col
    );

    if (seatIndex > -1) {
      setSelectedSeats((prevSeats) =>
        prevSeats.filter((seat) => !(seat.row === row && seat.col === col))
      );
    } else {
      setSelectedSeats((prevSeats) => [...prevSeats, { row, col }]);
    }
  };

  const isSeatSelected = (row, col) => {
    return selectedSeats.some((seat) => seat.row === row && seat.col === col);
  };

  // Helper function to check if a seat is disabled
  const isSeatDisabled = (row, col) => {
    return nonAvaliableSeats.some((seat) => seat === row * 1000 + col);
  };

  return (
    <div className=" absolute inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white p-4 rounded w-[60%] h-[60%] space-x-2 grid grid-cols-4">
        <div className="col-span-3 border-r border-gray-400 px-3 flex flex-col justify-between py-7 items-center">
          <div className="items-center text-center">
            <h2>Details</h2>
            <p>Name: {busData.bus_name}</p>
            <p>ID: {busData.id}</p>
            <p className="bg-green-500 p-2 rounded-md">
              Fare: {busData.fare * selectedSeats.length}
            </p>
            <p></p>
          </div>
          <div className="bg-orange-300 border p-5 rounded-md">
            Seats:
            {selectedSeats.map((value, index) => {
              return (
                <span key={index}>{`${value.row * 1000 + value.col}, `}</span>
              );
            })}
          </div>
          <div className="flex flex-row w-full items-center justify-evenly ">
            {showConfirm ? (
              <>
                <button
                  onClick={cancelSeats}
                  className="mt-4 px-4 py-2 mx-5 bg-red-500 text-white rounded"
                >
                  Cancel
                </button>
                <button
                  onClick={bookSeats}
                  className="mt-4 px-4 py-2 mx-5 bg-blue-500 text-white rounded"
                >
                  Pay
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={onClose}
                  className="mt-4 px-4 py-2 bg-red-800 text-white rounded"
                >
                  Close
                </button>
                <button
                  onClick={lockSeats}
                  className="mt-4 px-4 py-2 bg-green-500 text-white rounded"
                >
                  Book
                </button>
              </>
            )}
          </div>
        </div>

        <div
          className="grid gap-0"
          style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}
        >
          {[...Array(rows)].map((_, rowIndex) => (
            <React.Fragment key={rowIndex}>
              {[...Array(cols)].map((_, colIndex) => (
                <div
                  key={`${rowIndex}-${colIndex}`}
                  className="flex items-center justify-center"
                >
                  <input
                    type="checkbox"
                    className="w-3.5 h-3.5 checkbox-container bg-yellow-400"
                    checked={isSeatSelected(rowIndex, colIndex)}
                    disabled={isSeatDisabled(rowIndex, colIndex)}
                    onChange={() => toggleSeatSelection(rowIndex, colIndex)}
                  />
                </div>
              ))}
            </React.Fragment>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Modal;
