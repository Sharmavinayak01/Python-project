import { useEffect, useState } from "react";

import "./App.css";

import ChatArea from "./components/ChatArea/ChatArea";
import ChatInput from "./components/ChatInput/ChatInput";

import {
  sendMessage,
  getChats,
  getChatMessages,
} from "./services/api";


function App() {

  // ==========================================
  // State
  // ==========================================

  const [messages, setMessages] = useState([]);

  const [chatId, setChatId] = useState(null);

  const [chatHistory, setChatHistory] = useState([]);

  const [loading, setLoading] = useState(false);

  const [historyLoading, setHistoryLoading] =
    useState(false);


  // ==========================================
  // Load Chat History
  // ==========================================

  const loadChatHistory = async () => {

    try {

      setHistoryLoading(true);

      const chats = await getChats();

      setChatHistory(chats);

    } catch (error) {

      console.error(
        "Chat History Error:",
        error
      );

    } finally {

      setHistoryLoading(false);

    }
  };


  // ==========================================
  // Load History When App Starts
  // ==========================================

  useEffect(() => {

    loadChatHistory();

  }, []);


  // ==========================================
  // Send Message
  // ==========================================

  const handleSend = async (message) => {

    try {

      setLoading(true);


      // Show user message immediately
      setMessages((prev) => [

        ...prev,

        {
          role: "user",
          content: message,
        },

      ]);


      // Send message to backend
      const data = await sendMessage(
        message,
        chatId
      );


      // Save chat ID
      setChatId(data.chat_id);


      // Show AI response
      setMessages((prev) => [

        ...prev,

        {
          role: "assistant",
          content: data.reply,
        },

      ]);


      // Refresh sidebar history
      await loadChatHistory();


    } catch (error) {

      console.error(
        "Chat Error:",
        error
      );


      setMessages((prev) => [

        ...prev,

        {
          role: "assistant",
          content:
            "Sorry, something went wrong.",
        },

      ]);

    } finally {

      setLoading(false);

    }

  };


  // ==========================================
  // Open Previous Chat
  // ==========================================

  const handleOpenChat = async (selectedChatId) => {

    try {

      setLoading(true);


      const data =
        await getChatMessages(
          selectedChatId
        );


      // Set selected chat ID
      setChatId(selectedChatId);


      // Load messages
      setMessages(data.messages);


    } catch (error) {

      console.error(
        "Open Chat Error:",
        error
      );

    } finally {

      setLoading(false);

    }

  };


  // ==========================================
  // New Chat
  // ==========================================

  const handleNewChat = () => {

    setChatId(null);

    setMessages([]);

  };


  // ==========================================
  // JSX
  // ==========================================

  return (

    <div className="app">


      {/* ======================================
          LEFT SIDEBAR
      ====================================== */}

      <aside className="sidebar">


        {/* Logo */}

        <div className="logo">

          <div className="logo-orb">
            ✦
          </div>

          <div>

            <h2>NEXA</h2>

            <span>
              AI ASSISTANT
            </span>

          </div>

        </div>


        {/* New Chat */}

        <button
          className="new-chat"
          onClick={handleNewChat}
        >

          <span>＋</span>

          New Chat

        </button>


        {/* Navigation */}

        <div className="navigation">

          <div className="nav-item active">
            <span>⌂</span>
            Home
          </div>

          <div className="nav-item">
            <span>◷</span>
            Chat History
          </div>

          <div className="nav-item">
            <span>✦</span>
            Prompts
          </div>

          <div className="nav-item">
            <span>⚙</span>
            Settings
          </div>

        </div>


        {/* Recent Chats */}

        <div className="recent-title">
          Recent Chats
        </div>


        <div className="recent-chats">

          {historyLoading ? (

            <div className="history-loading">
              Loading chats...
            </div>

          ) : chatHistory.length === 0 ? (

            <div className="history-empty">
              No chats yet
            </div>

          ) : (

            chatHistory.map((chat) => (

              <div
                key={chat.chat_id}
                className={`chat-history-item ${
                  chat.chat_id === chatId
                    ? "selected-chat"
                    : ""
                }`}
                onClick={() =>
                  handleOpenChat(
                    chat.chat_id
                  )
                }
              >

                <span>💬</span>

                <span className="chat-title">
                  {chat.title}
                </span>

              </div>

            ))

          )}

        </div>


        {/* Profile */}

        <div className="profile">

          <div className="profile-avatar">
            K
          </div>

          <div>

            <strong>
              Kunal
            </strong>

            <small>
              Online
            </small>

          </div>

        </div>

      </aside>


      {/* ======================================
          MAIN AREA
      ====================================== */}

      <main className="main-area">


        {/* Welcome */}

        <div className="welcome-section">

          <div className="ai-orb">

            <div className="orb-core">
              ◉
            </div>

          </div>

          <h1>
            Hello, <span>Kunal</span> 👋
          </h1>

          <p>
            I'm NEXA — Your AI Assistant
          </p>

          <small>
            Ask anything, explore ideas,
            write, code, learn and more.
          </small>

        </div>


        {/* Chat */}

        <ChatArea
          messages={messages}
        />


        {/* Input */}

        <ChatInput
          onSend={handleSend}
          loading={loading}
        />

      </main>


      {/* ======================================
          RIGHT PANEL
      ====================================== */}

      <aside className="right-panel">


        {/* Model */}

        <div className="panel-card">

          <h3>
            AI Model
          </h3>

          <div className="model-box">

            <strong>
              GPT OSS 120B
            </strong>

            <span className="online">
              ● Online
            </span>

          </div>

        </div>


        {/* Tools */}

        <div className="panel-card">

          <h3>
            Quick Tools
          </h3>

          <button>
            ✦ Generate
          </button>

          <button>
            ⚡ Analyze
          </button>

          <button>
            ✎ Rewrite
          </button>

        </div>


        {/* Stats */}

        <div className="panel-card">

          <h3>
            Today's Stats
          </h3>

          <div className="stats-grid">

            <div>

              <strong>
                {messages.length}
              </strong>

              <span>
                Messages
              </span>

            </div>

            <div>

              <strong>
                {chatHistory.length}
              </strong>

              <span>
                Chats
              </span>

            </div>

            <div>

              <strong>
                AI
              </strong>

              <span>
                Active
              </span>

            </div>

          </div>

        </div>


        {/* Quote */}

        <div className="quote-card">

          <span>
            “
          </span>

          <p>
            The best way to predict the
            future is to create it.
          </p>

          <small>
            — Peter Drucker
          </small>

        </div>

      </aside>

    </div>

  );

}


export default App;