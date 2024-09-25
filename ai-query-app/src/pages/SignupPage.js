import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // Import Axios for making API requests

function SignupPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const navigate = useNavigate(); // Initialize the navigate hook

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password || !confirmPassword) {
      setError('All fields are required');
      setSuccess(false);
    } else if (password !== confirmPassword) {
      setError('Passwords do not match');
      setSuccess(false);
    } else {
      setError(''); // Clear error message before the request
      try {
        const response = await axios.post('http://localhost:5000/sign-up', {
          username,
          password
        });
  
        if (response.status === 201) {
          // Success
          setSuccess(true);
          setError('');
          setTimeout(() => {
            navigate('/login'); // Redirect to login page after success
          }, 2000);
        }
      } catch (err) {
        // Handle error response
        if (err.response && err.response.status === 400) {
          setError(err.response.data.message); // Username already exists
        } else {
          setError('Signup failed. Please try again.');
        }
        setSuccess(false);
      }
    }
  };
  

  const handleSignupRedirect = () => {
    navigate('/login'); // Redirect to the login page
  };

  return (
    <div className="min-h-screen bg-black flex flex-col justify-center items-center text-white">
      <header className="text-center mb-8 mt-4">
        <h1 className="text-5xl font-extrabold text-gray-200">Sign Up</h1>
        <p className="text-gray-400 mt-2">Create a new account</p>
      </header>

      {/* Form to submit username, password, and confirm password */}
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

        <div className="mb-6">
          <label className="block text-gray-400 text-sm font-semibold mb-2">Confirm Password:</label>
          <input
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Re-enter your password"
            required
          />
        </div>

        <button
          type="submit"
          className={`w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition duration-200 shadow-lg`}
        >
          Sign Up
        </button>
      </form>

      {/* Display error message */}
      {error && (
        <div className="mt-4 bg-red-600 p-4 rounded-lg shadow-md text-center">
          <p>{error}</p>
        </div>
      )}

      {/* Display success message */}
      {success && (
        <div className="mt-4 bg-green-600 p-4 rounded-lg shadow-md text-center">
          <p>Account created successfully! Redirecting to login...</p>
        </div>
      )}

      {/* Already have an account? Log in link */}
      <div className="mt-4 text-gray-400">
        <p>
          Already have an account?{' '}
          <button onClick={handleSignupRedirect} className="text-purple-500 hover:text-purple-400 underline">
            Log in
          </button>
        </p>
      </div>
    </div>
  );
}

export default SignupPage;
