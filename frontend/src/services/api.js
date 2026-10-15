const API_URL = "http://127.0.0.1:5000";


// ==========================================
// Send Message
// ==========================================

export async function sendMessage(message, chatId = null) {
  const response = await fetch(`${API_URL}/chat`, {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
    },

    body: JSON.stringify({
      message,
      chat_id: chatId,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Something went wrong"
    );
  }

  return data;
}


// ==========================================
// Get Chat History
// ==========================================

export async function getChats() {
  const response = await fetch(
    `${API_URL}/chats`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Unable to load chats"
    );
  }

  return data;
}


// ==========================================
// Get Specific Chat Messages
// ==========================================

export async function getChatMessages(chatId) {
  const response = await fetch(
    `${API_URL}/chats/${chatId}`
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.error || "Unable to load chat"
    );
  }

  return data;
}