import { Routes, Route, useLocation } from "react-router-dom";
import Home from "./component/home";
import LoginPage from "./component/login";
import BookingsPage from "./component/bookings";
import NavBar from "./component/NavBar"

function App() {
  const location = useLocation();
  return (
    <>
      {location.pathname !== "/login" && <NavBar />}
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/login" element={<LoginPage/>} />
        <Route path="/bookings" element={<BookingsPage/>}/>
      </Routes>
    </>
  );
}

export default App;
