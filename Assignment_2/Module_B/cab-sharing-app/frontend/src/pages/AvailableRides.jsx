import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

// --- Sub-component: A single Ride Card ---
const RideCard = ({ ride }) => {
    // This state controls whether the extra details are visible for THIS specific card
    const [showDetails, setShowDetails] = useState(false);

    return (
        <div style={{ border: '1px solid #ccc', color: 'black', borderRadius: '8px', padding: '15px', marginBottom: '15px', backgroundColor: '#f9f9f9' }}>
            <h3 style={{ marginTop: '0' }}>{ride.Source} ➔ {ride.Destination}</h3>

            <p style={{ margin: '5px 0' }}><strong>Time:</strong> {new Date(ride.StartTime).toLocaleString()}</p>
            <p style={{ margin: '5px 0' }}><strong>Host ID:</strong> {ride.AdminID}</p>

            {/* Action Buttons */}
            <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                <button style={{ padding: '8px 12px', background: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Join Request
                </button>
                <button style={{ padding: '8px 12px', background: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Chat
                </button>
                <button
                    onClick={() => setShowDetails(!showDetails)}
                    style={{ padding: '8px 12px', background: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
                >
                    {showDetails ? 'Hide Details' : 'View Details'}
                </button>
            </div>

            {/* Hidden Details Section */}
            {showDetails && (
                <div style={{ marginTop: '15px', padding: '10px', borderTop: '1px solid #ddd' }}>
                    <p style={{ margin: '5px 0' }}><strong>Available Seats:</strong> {ride.AvailableSeats}</p>
                    <p style={{ margin: '5px 0' }}><strong>Current Passengers:</strong> {ride.PassengerCount}</p>
                    <p style={{ margin: '5px 0' }}><strong>Vehicle:</strong> {ride.VehicleType}</p>
                    <p style={{ margin: '5px 0' }}><strong>Est. Duration:</strong> {ride.EstimatedTime} mins</p>
                    {ride.FemaleOnly ? <p style={{ margin: '5px 0', color: '#d63384', fontWeight: 'bold' }}>♀ Female Only Ride</p> : null}
                </div>
            )}
        </div>
    );
};

// --- Main Page Component ---
const AvailableRides = () => {
    const [rides, setRides] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        // MOCK API RESPONSE (Based directly on your database schema)
        const mockRidesFromAPI = [
            {
                RideID: 101,
                AdminID: 42,
                PassengerCount: 1,
                AvailableSeats: 3,
                Source: "Campus Main Gate",
                Destination: "City Mall",
                VehicleType: "Car",
                StartTime: "2023-11-15T14:30:00",
                EstimatedTime: 45,
                FemaleOnly: false
            },
            {
                RideID: 102,
                AdminID: 88,
                PassengerCount: 2,
                AvailableSeats: 0,
                Source: "Hostel Block B",
                Destination: "Railway Station",
                VehicleType: "Auto Rickshaw",
                StartTime: "2023-11-16T08:00:00",
                EstimatedTime: 20,
                FemaleOnly: true
            }
        ];

        // Simulate a 1-second network delay from FastAPI
        setTimeout(() => {
            setRides(mockRidesFromAPI);
            setLoading(false);
        }, 1000);
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('isAuthenticated');
        navigate('/login');
    };

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <h2>Available Campus Rides</h2>
                {/* <button onClick={handleLogout} style={{ padding: '8px 15px', background: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    Logout
                </button> */}
            </div>

            {loading ? (
                <p>Loading rides from server...</p>
            ) : (
                <div>
                    {rides.length === 0 ? (
                        <p>No active rides found right now.</p>
                    ) : (
                        rides.map(ride => <RideCard key={ride.RideID} ride={ride} />)
                    )}
                </div>
            )}
        </div>
    );
};

export default AvailableRides;