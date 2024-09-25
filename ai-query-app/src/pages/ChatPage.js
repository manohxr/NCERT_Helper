import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios'; // Import Axios for API requests
import Latex from 'react-latex-next'; // Import Latex rendering
import 'katex/dist/katex.min.css'; // Import KaTeX CSS for styling

function ChatPage() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]); // State to store chat history
  const [loading, setLoading] = useState(false); // State for loading
  const [error, setError] = useState(''); // State for handling errors
  const messagesEndRef = useRef(null); // Reference for automatic scroll

  // Function to scroll to the bottom of the chat
  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return; // Prevent empty submissions
  
    const username = localStorage.getItem('userName'); // Retrieve username from localStorage
    if (!username) {
      setError('User is not logged in.');
      return;
    }
  
    setLoading(true); // Set loading to true when starting the request
    setError(''); // Reset error state
  
    const userMessage = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMessage]); // Add user message to the chat history
  
    try {
      const res = await axios.post('http://localhost:5000/query', { query, username }); // Send the query along with user_id to the Flask back-end
      const botMessage = { role: 'bot', content: res.data.answer }; // Get AI response
      setMessages((prev) => [...prev, botMessage]); // Add bot response to chat history
    } catch (err) {
      setError('Error fetching response. Please try again later.'); // Handle errors
    } finally {
      setLoading(false); // Stop loading after request is done
    }
  
    setQuery(''); // Reset the query input after submission
  };
  

  return (
    <div className="min-h-screen bg-black flex flex-col justify-center items-center text-white">
      <header className="text-center mb-8 mt-4">
        <h1 className="text-5xl font-extrabold text-gray-200">NCERT Helper</h1>
        <p className="text-gray-400 mt-2">Ask your questions and get AI-powered answers!</p>
      </header>

      {/* Chat messages display */}
      <div className="bg-gray-900 p-8 shadow-lg rounded-lg max-w-md w-full border border-purple-500 mb-6 h-96 overflow-y-auto">
        {messages.length > 0 ? (
          messages.map((msg, index) => (
            <div key={index} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
              <p className={`p-2 rounded-lg inline-block ${msg.role === 'user' ? 'bg-purple-700' : 'bg-gray-800'} text-white`}>
                {msg.role === 'bot' ? <Latex>{msg.content}</Latex> : msg.content}
              </p>
            </div>
          ))
        ) : (
          <p className="text-gray-400 text-center">Start a conversation!</p>
        )}
        {/* Ref element to scroll to the latest message */}
        <div ref={messagesEndRef} />
      </div>

      {/* Form to submit a new query */}
      <form onSubmit={handleSubmit} className="bg-gray-900 p-8 shadow-lg mb-4 rounded-lg max-w-md w-full border border-purple-500">
        <div className="mb-6">
          <label className="block text-gray-400 text-sm font-semibold mb-2">Enter your query:</label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full p-3 bg-gray-800 border border-gray-700 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500"
            placeholder="Type your question..."
            required
          />
        </div>

        <button
          type="submit"
          className={`w-full bg-purple-600 text-white py-2 rounded-lg hover:bg-purple-700 transition duration-200 shadow-lg ${loading ? 'opacity-50' : ''}`}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Submit'}
        </button>
      </form>

      {/* Display error message */}
      {error && (
        <div className="mt-4 bg-red-600 p-4 rounded-lg shadow-md text-center">
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}

export default ChatPage;
