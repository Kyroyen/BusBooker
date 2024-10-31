import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();
  const handleLogout = () => {
    // Clear authentication tokens or any user data from storage
    localStorage.removeItem("authToken"); // Adjust as per your token key
    navigate("/login"); // Navigate to login page
  };
  return (
    <nav className="bg-gray-800 p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-white text-lg">
          <Link to="/" className="hover:text-gray-300">
            Home
          </Link>
        </div>
        <div className="flex space-x-4">
          <div onClick={handleLogout} className="text-white hover:text-gray-300 cursor-pointer">Logout</div>

          <Link to="/bookings" className="text-white hover:text-gray-300">
            Bookings
          </Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
