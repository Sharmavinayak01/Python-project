import { useEffect, useRef } from "react";
import ChatMessage from "../ChatMessage/ChatMessage";
import "./ChatArea.css";

function ChatArea({ messages }) {
  const messagesContainerRef = useRef(null);

  useEffect(() => {
    const container = messagesContainerRef.current;

    if (!container) return;

    // New message ke baad bottom par scroll
    container.scrollTop = container.scrollHeight;

  }, [messages]);

  return (
    <div className="chat-area">

      {/* Chat Header */}
      <div className="chat-header">
        <div>
          <h2>NEXA AI</h2>
          <span>● Online</span>
        </div>
      </div>


      {/* Messages */}
      <div
        className="messages-container"
        ref={messagesContainerRef}
      >

        {messages.length === 0 ? (

          <div className="empty-chat">
            Start a conversation with NEXA ✦
          </div>

        ) : (

          messages.map((message, index) => (
            <ChatMessage
              key={index}
              role={message.role}
              content={message.content}
            />
          ))

        )}

      </div>

    </div>
  );
}

export default ChatArea;