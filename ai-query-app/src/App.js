import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import ChatPage from './pages/ChatPage';

function App() {
  return (
    <div>
      <Routes>
        <Route path="/" element={
          <div className="min-h-screen bg-black flex flex-col justify-center items-center text-white">
            <header className="text-center mb-8">
              <h1 className="text-5xl font-extrabold text-gray-200">Welcome to NCERT Helper</h1>
              <p className="text-gray-400 mt-2">Please log in to continue</p>
            </header>

            <div className="bg-gray-900 p-8 shadow-lg rounded-lg max-w-md w-full border border-purple-500">
              <Link to="/login">
                <button className="w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition duration-200 shadow-lg">
                  Go to Login Page
                </button>
              </Link>
            </div>
          </div>
        } />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/sign-up" element={<SignupPage />} />
        <Route path="/chat" element={<ChatPage />} />
      </Routes>
    </div>
  );
}

export default App;
