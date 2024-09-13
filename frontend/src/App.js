import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css'; // Custom styles

const App = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [options, setOptions] = useState([]);
    const [userId, setUserId] = useState('12345'); // Static user ID for now
    const chatBoxRef = useRef(null); // Ref for the chat box container

    // Load chat session from localStorage
    useEffect(() => {
        const savedMessages = JSON.parse(localStorage.getItem('messages')) || [];
        const savedOptions = JSON.parse(localStorage.getItem('options')) || [];
        setMessages(savedMessages.length > 0 ? savedMessages : [{ from: 'bot', text: 'Hi, what is your name?' }]);
        setOptions(savedOptions);
    }, []);

    // Save chat session to localStorage on message or options update
    useEffect(() => {
        localStorage.setItem('messages', JSON.stringify(messages));
        localStorage.setItem('options', JSON.stringify(options));

        // Auto-scroll to the last message when messages change
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [messages, options]);

    const sendMessage = (message) => {
        const newMessages = [...messages, { from: 'user', text: message }];
        setMessages(newMessages);
        setInput('');

        axios.post('http://localhost:5000/chat', { user_id: userId, message })
            .then(response => {
                const { response: botMessage, options, marks } = response.data;

                // Add bot's response to the chat
                setMessages(prev => [...prev, { from: 'bot', text: botMessage }]);

                // If marks are available, display them as separate messages
                if (marks) {
                    marks.forEach(mark => {
                        setMessages(prev => [...prev, { from: 'bot', text: mark }]);
                    });
                }

                // If options exist, display them as buttons
                if (options) {
                    setOptions(options);
                } else {
                    setOptions([]); // Clear options if none are available
                }
            })
            .catch(error => {
                console.error(error);
            });
    };

    const handleOptionClick = (option) => {
        sendMessage(option);
        setOptions([]); // Clear the options after one is clicked
    };

    return (
        <div className="chat-container">
            <div className="chat-box" ref={chatBoxRef}>
                {messages.map((msg, index) => (
                    <div key={index} className={`message ${msg.from}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            {options.length > 0 && (
                <div className="options">
                    {options.map(option => (
                        <button
                            key={option}
                            className="option-button"
                            onClick={() => handleOptionClick(option)}
                        >
                            {option}
                        </button>
                    ))}
                </div>
            )}
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage(input)}
                    placeholder="Type a message..."
                    disabled={options.length > 0} // Disable text input if there are options
                />
                <button onClick={() => sendMessage(input)} disabled={options.length > 0}>Send</button>
            </div>
        </div>
    );
};

export default App;
