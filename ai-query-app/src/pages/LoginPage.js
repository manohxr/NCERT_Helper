import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import Axios for making API requests

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate(); // Initialize the navigate hook

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Both fields are required');
      return;
    }
  
    setError(''); // Clear error before API call
    try {
      const response = await axios.post('http://localhost:5000/login', {
        username,
        password
      });
  
      if (response.status === 200) {
        const userName = response.data.username; // Use the username from the backend response
        localStorage.setItem('userName', userName); // Store username in local storage
        navigate('/chat'); // Redirect to chat page after successful login
      }
    } catch (err) {
      if (err.response && err.response.status === 401) {
        setError(err.response.data.message); // Show "Invalid credentials" from backend
      } else {
        setError('Login failed. Please try again.'); // Handle other errors
      }
    }
  };
  
  const handleSignupRedirect = () => {
    navigate('/sign-up'); // Redirect to the signup page
  };
  

  return (
    <div className="min-h-screen bg-black flex flex-col justify-center items-center text-white">
      <header className="text-center mb-8 mt-4">
        <h1 className="text-5xl font-extrabold text-gray-200">Login</h1>
        <p className="text-gray-400 mt-2">Please enter your credentials to continue</p>
      </header>

      {/* Form to submit username and password */}
      <form onSubmit={handleSubmit} className="bg-gray-900 p-8 shadow-lg mb-4 rounded-lg max-w-md w-full border border-purple-500">
        <div className="mb-6">
          <label className="block text-gray-400 text-sm font-semibold mb-2">Username:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Enter your username"
            required
          />
        </div>

        <div className="mb-6">
          <label className="block text-gray-400 text-sm font-semibold mb-2">Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Enter your password"
            required
          />
        </div>

        <button
          type="submit"
          className={`w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition duration-200 shadow-lg`}
        >
          Login
        </button>
      </form>

      {/* Display error message */}
      {error && (
        <div className="mt-4 bg-red-600 p-4 rounded-lg shadow-md text-center">
          <p>{error}</p>
        </div>
      )}

      {/* Don't have an account? Sign up link */}
      <div className="mt-4 text-gray-400">
        <p>
          Don't have an account?{' '}
          <button onClick={handleSignupRedirect} className="text-purple-500 hover:text-purple-400 underline">
            Sign up
          </button>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
