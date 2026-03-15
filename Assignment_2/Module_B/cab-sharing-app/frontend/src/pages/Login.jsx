import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = (e) => {
        e.preventDefault();
        // This is where you'll eventually talk to FastAPI.
        // For now, let's just "fake" a successful login.
        if (email && password) {
            localStorage.setItem('isAuthenticated', 'true');
            navigate('/available-rides');
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '100px auto', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
            <h2>Campus Ride Share</h2>
            <form onSubmit={handleLogin}>
                <div style={{ marginBottom: '15px' }}>
                    <label>Email:</label><br />
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: '100%' }} required />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <label>Password:</label><br />
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: '100%' }} required />
                </div>
                <button type="submit" style={{ width: '100%', padding: '10px', background: '#007bff', color: 'white', border: 'none', borderRadius: '4px' }}>
                    Login
                </button>
            </form>
        </div>
    );
};

export default Login;