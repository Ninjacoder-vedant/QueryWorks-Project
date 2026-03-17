import React, { useState } from 'react';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';

function Login() {
  const navigate = useNavigate();
  // State to handle button loading UI and error messages
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const login = useGoogleLogin({
    onSuccess: async (codeResponse) => {
      setIsLoading(true);
      setErrorMessage(''); // Clear any previous errors
      
      try {
        // 1. Send the authorization code to your FastAPI backend
        const response = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code: codeResponse.code }),
        });

        const data = await response.json();

        if (response.ok) {
          // 2. Set authentication flags
          localStorage.setItem('isAuthenticated', 'true');
          localStorage.setItem('user', JSON.stringify(data.user)); 

          // 3. Redirect the user into the cab sharing portal
          navigate('/available-rides');
        } else {
          // If FastAPI throws an HTTPException (like a non-university email)
          setErrorMessage(data.detail || 'Backend validation failed. Please try again.');
          console.error('Backend validation failed:', data);
        }
      } catch (error) {
        setErrorMessage('Cannot connect to the server. Make sure FastAPI is running!');
        console.error('Error connecting to backend:', error);
      } finally {
        setIsLoading(false);
      }
    },
    onError: (errorResponse) => {
      // This catches the silent popup errors!
      setErrorMessage('Google Login popup failed or was closed.');
      console.error('Google Login Error:', errorResponse);
      setIsLoading(false);
    },
    flow: 'auth-code',
  });

  return (
    <div style={{ textAlign: 'center', marginTop: '100px', fontFamily: 'sans-serif' }}>
      <h2>Welcome to the Cab Sharing Portal</h2>
      <p>Please sign in with your university account to continue.</p>
      
      {/* Display errors to the user if anything goes wrong */}
      {errorMessage && (
        <div style={{ color: 'red', marginBottom: '15px', padding: '10px', backgroundColor: '#fee' }}>
          {errorMessage}
        </div>
      )}
      
      <button 
        onClick={() => login()}
        disabled={isLoading}
        style={{ 
          padding: '10px 20px', 
          fontSize: '16px', 
          cursor: isLoading ? 'not-allowed' : 'pointer',
          backgroundColor: isLoading ? '#ccc' : '#4285F4',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        {isLoading ? 'Signing in...' : 'Sign in with Google'}
      </button>
    </div>
  );
}

export default Login;