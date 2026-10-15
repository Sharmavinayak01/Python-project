import { useState } from "react";
import "./ChatInput.css";

function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const trimmedMessage = message.trim();

    if (!trimmedMessage || loading) {
      return;
    }

    await onSend(trimmedMessage);

    setMessage("");
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      
      <button type="button" className="input-icon">
        ＋
      </button>

      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask NEXA anything..."
        disabled={loading}
      />

      <button type="button" className="input-icon">
        🌐
      </button>

      <button type="button" className="tool-button">
        ✧ Tools
      </button>

      <button type="button" className="mic-button">
        🎤
      </button>

      <button
        type="submit"
        className="send-button"
        disabled={loading}
      >
        {loading ? "..." : "➤"}
      </button>

    </form>
  );
}

export default ChatInput;