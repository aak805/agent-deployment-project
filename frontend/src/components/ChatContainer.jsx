// src/components/ChatContainer.jsx
import React, { useState, useEffect } from 'react';
import ChatInput from './ChatInput';

const ChatContainer = () => {
  const [messages, setMessages] = useState([]);
  const [threadId, setThreadId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // This is the function that talks to your FastAPI backend
  const sendMessage = async (message) => {
    setIsLoading(true);
    try {
      const payload = {
        message: message,
        thread_id: threadId,
      };

      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setMessages(data.messages);
      setThreadId(data.thread_id);

    } catch (error) {
      console.error("Failed to send message:", error);
    } finally {
      setIsLoading(false);
    }
  };

  // This useEffect will run once to start the conversation.
  useEffect(() => {
    // Check if the conversation has started
    if (messages.length === 0) {
      sendMessage('');
    }
  }, [messages]);  
                 // This is a subtle change but more robust for handling the initial call.

  return (
    <div className="chat-container">
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
        {isLoading && <div>Loading...</div>}
      </div>
      <ChatInput sendMessage={sendMessage} />
    </div>
  );
};

export default ChatContainer;