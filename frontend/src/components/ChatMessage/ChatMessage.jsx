import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./ChatMessage.css";

function ChatMessage({ role, content }) {
  const isUser = role === "user";

  return (
    <div className={`message-row ${isUser ? "user-row" : "ai-row"}`}>
      
      {!isUser && (
        <div className="message-avatar">
          ✦
        </div>
      )}

      <div
        className={`message-bubble ${
          isUser ? "user-message" : "ai-message"
        }`}
      >
        {isUser ? (
          content
        ) : (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        )}
      </div>

      {isUser && (
        <div className="message-avatar user-avatar">
          K
        </div>
      )}
    </div>
  );
}

export default ChatMessage;