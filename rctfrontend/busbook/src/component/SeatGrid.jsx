import React, { useState } from 'react';

function SeatGrid({ rows, cols }) {
  // State to hold selected seats
  const [selectedSeats, setSelectedSeats] = useState([]);

  // Handle seat click
  const toggleSeatSelection = (row, col) => {
    const seatIndex = selectedSeats.findIndex(seat => seat.row === row && seat.col === col);

    if (seatIndex > -1) {
      // Seat is already selected, so remove it
      setSelectedSeats(prevSeats => prevSeats.filter(seat => !(seat.row === row && seat.col === col)));
    } else {
      // Seat is not selected, so add it
      setSelectedSeats(prevSeats => [...prevSeats, { row, col }]);
    }
  };

  return (
    <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
      {[...Array(rows)].map((_, rowIndex) => (
        <React.Fragment key={rowIndex}>
          {[...Array(cols)].map((_, colIndex) => (
            <div key={`${rowIndex}-${colIndex}`} className="flex items-center justify-center">
              <input
                type="checkbox"
                className="w-6 h-6"
                checked={selectedSeats.some(seat => seat.row === rowIndex && seat.col === colIndex)}
                onChange={() => toggleSeatSelection(rowIndex, colIndex)}
              />
            </div>
          ))}
        </React.Fragment>
      ))}
      {/* Display selected seats */}
      <div className="col-span-full mt-4 p-2 bg-gray-100 rounded">
        <h3 className="text-lg font-semibold">Selected Seats:</h3>
        <ul className="list-disc pl-5">
          {selectedSeats.map((seat, index) => (
            <li key={index}>
              Row {seat.row + 1}, Column {seat.col + 1}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default SeatGrid;
