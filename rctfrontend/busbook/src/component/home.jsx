import React, { useEffect, useState } from "react";
import axiosInstance from "../api/axiosInstance.js";
import BusListComponent from "./BusListComponent.jsx";
import Modal from "./Modal.jsx";

function Home() {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [results, setResults] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedBus, setSelectedBus] = useState(null);

  const handleOpenModal = (bus) => {
    console.log("open Modal", bus);

    setSelectedBus(bus);
    setIsModalOpen(true);
  };
  const handleCloseModal = () => {
    handleSearch();
    setIsModalOpen(false);
    setSelectedBus(null);
  };

  const handleSearch = async () => {
    if (start === "" || end === "") {
      alert("Please enter both start and end points");
      return;
    }
    try {
      const response = await axiosInstance.get("routes", {
        params: { start, end },
      });
      setResults(response.data);
      console.log(results);
    } catch (error) {
      console.error("Search failed", error);
    }
  };

  return (
    <div>
      <div className="flex items-center justify-center space-x-2 bg-cyan-50 py-10">
        <input
          type="text"
          placeholder="Start"
          value={start}
          onChange={(e) => setStart(e.target.value)}
          required
          className="border flex border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input
          type="text"
          placeholder="End"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
          required
          className="border flex border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          onClick={(e) => handleSearch(e)}
          className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
        >
          Search
        </button>
      </div>

      {(results.length !== 0) ? (
        <div className="w-full justify-center flex">
          <div className="w-[70%] flex flex-col items-center text-center justify-center space-y-2 py-5 ">
            <div className="w-full rounded-lg p-4 mb-4 flex flex-row space-x-5 justify-between">
              <span> SrNo. </span>
              <span>Name</span>
              <span>Start Time</span>
              <span>End Time</span>
              <span>Fare</span>
              <span>Date</span>
              <span>Seats Left</span>
            </div>
            <div className="w-full text-center">
              {results.map((bus) => {
                return (
                  <BusListComponent
                    key={bus.id}
                    busData={bus}
                    onClick={handleOpenModal}
                  />
                );
              })}
            </div>
          </div>
        </div>
      ) : (
        <div className="flex w-full justify-center py-10">NO RECORDS</div>
      )}

      {isModalOpen && (
        <Modal busData={selectedBus} onClose={handleCloseModal} />
      )}
    </div>
  );
}

export default Home;
