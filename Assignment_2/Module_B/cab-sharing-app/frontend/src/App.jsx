import React from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom'; 

// Import your components
import Login from './pages/Login';
import AvailableRides from './pages/AvailableRides';
import PrivateRoute from './components/PrivateRoute';
import Navbar from './components/Navbar'; 

function App() {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  const location = useLocation(); // 2. This hook tells us what page we are on

  // 3. Hide the Navbar if we are on the login page or the root ("/") page
  const showNavbar = location.pathname !== '/login' && location.pathname !== '/';

  return (
    <>
      {/* 4. Render the Navbar right above your routes */}
      {showNavbar && <Navbar isLoggedIn={isAuthenticated} />}

      <Routes>
        <Route
          path="/"
          element={
            isAuthenticated ? (
              <Navigate to="/available-rides" />
            ) : (
              <Navigate to="/login" />
            )
          }
        />

        <Route path="/login" element={<Login />} />

        <Route
          path="/available-rides"
          element={
            <PrivateRoute>
              <AvailableRides />
            </PrivateRoute>
          }
        />

        <Route path="*" element={<h2>404 - Page Not Found</h2>} />
      </Routes>
    </>
  );
}

export default App;