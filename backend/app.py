from flask import Flask, request, jsonify 
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime, timezone
from dotenv import load_dotenv
from groq import Groq
import os
import uuid


# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()


# ==========================================
# Flask App
# ==========================================

app = Flask(__name__)

# Allow React frontend to communicate with Flask
CORS(app)


# ==========================================
# Groq AI
# ==========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================
# MongoDB
# ==========================================

mongo_client = MongoClient(
    os.getenv("MONGODB_URI")
)

db = mongo_client["ai_chatbot"]

# Chat information
chats_collection = db["chats"]

# Individual messages
messages_collection = db["messages"]


# ==========================================
# Helper Functions
# ==========================================

def current_time():
    """
    Current UTC time.
    """
    return datetime.now(timezone.utc)


def is_greeting(message):
    """
    Check whether the user message is only a greeting.
    """

    greetings = {
        "hi",
        "hii",
        "hiii",
        "hello",
        "hey",
        "hey there",
        "hi there",
        "hello there",
        "good morning",
        "good afternoon",
        "good evening",
        "good night"
    }

    # Remove spaces and punctuation
    cleaned_message = (
        message
        .strip()
        .lower()
        .replace("!", "")
        .replace(".", "")
        .replace(",", "")
        .replace("?", "")
    )

    return cleaned_message in greetings


def create_title(message):
    """
    Create a chat title from user's first meaningful question.
    """

    title = message.strip()

    # Maximum 50 characters
    if len(title) > 50:
        title = title[:50].strip() + "..."

    return title


# ==========================================
# Home Route
# ==========================================

@app.route("/")
def home():

    return "AI Chatbot Backend is Running!"


# ==========================================
# Chat Route
# ==========================================

@app.route("/chat", methods=["POST"])
def chat():

    try:

        # ----------------------------------
        # Get data from frontend
        # ----------------------------------

        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400

        message = data.get("message")
        chat_id = data.get("chat_id")


        # ----------------------------------
        # Check message
        # ----------------------------------

        if not message or not message.strip():

            return jsonify({
                "error": "Message is required"
            }), 400

        message = message.strip()


        # ----------------------------------
        # Create new chat
        # ----------------------------------

        if not chat_id:

            chat_id = str(uuid.uuid4())

            # Greeting ko title nahi banayenge
            if is_greeting(message):

                title = "New Conversation"

            else:

                title = create_title(message)


            # Create chat document
            chats_collection.insert_one({

                "chat_id": chat_id,

                "title": title,

                "created_at": current_time(),

                "updated_at": current_time()

            })


        # ----------------------------------
        # Get previous messages
        # ----------------------------------

        previous_messages = messages_collection.find(
            {
                "chat_id": chat_id
            }
        ).sort(
            "created_at",
            1
        )


        # ----------------------------------
        # Create conversation
        # ----------------------------------

        conversation = []


        for msg in previous_messages:

            conversation.append({

                "role": msg["role"],

                "content": msg["content"]

            })


        # ----------------------------------
        # Add current user message
        # ----------------------------------

        conversation.append({

            "role": "user",

            "content": message

        })


        # ----------------------------------
        # Send conversation to Groq
        # ----------------------------------

        completion = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=conversation

        )


        # ----------------------------------
        # Get AI response
        # ----------------------------------

        reply = completion.choices[0].message.content


        # ----------------------------------
        # Save user message
        # ----------------------------------

        messages_collection.insert_one({

            "chat_id": chat_id,

            "role": "user",

            "content": message,

            "created_at": current_time()

        })


        # ----------------------------------
        # Save AI response
        # ----------------------------------

        messages_collection.insert_one({

            "chat_id": chat_id,

            "role": "assistant",

            "content": reply,

            "created_at": current_time()

        })


        # ==================================
        # Update Chat History
        # ==================================

        chat = chats_collection.find_one({
            "chat_id": chat_id
        })


        if chat:

            current_title = chat.get(
                "title",
                "New Conversation"
            )


            # ----------------------------------
            # If current title is greeting
            # or New Conversation
            # ----------------------------------

            if (
                current_title == "New Conversation"
                or is_greeting(current_title)
            ):

                # Current message greeting nahi hai
                if not is_greeting(message):

                    chats_collection.update_one(

                        {
                            "chat_id": chat_id
                        },

                        {
                            "$set": {

                                "title": create_title(message),

                                "updated_at": current_time()

                            }
                        }

                    )

                else:

                    chats_collection.update_one(

                        {
                            "chat_id": chat_id
                        },

                        {
                            "$set": {

                                "updated_at": current_time()

                            }
                        }

                    )


            # ----------------------------------
            # Existing meaningful title
            # ----------------------------------

            else:

                chats_collection.update_one(

                    {
                        "chat_id": chat_id
                    },

                    {
                        "$set": {

                            "updated_at": current_time()

                        }
                    }

                )


        # ----------------------------------
        # Send response to frontend
        # ----------------------------------

        return jsonify({

            "chat_id": chat_id,

            "reply": reply

        })


    # ======================================
    # Error Handling
    # ======================================

    except Exception as e:

        print("CHAT ERROR:", e)

        return jsonify({

            "error": str(e)

        }), 500


# ==========================================
# Get All Chat History
# ==========================================

@app.route("/chats", methods=["GET"])
def get_chats():

    try:

        chats = chats_collection.find(
            {},

            {
                "_id": 0,

                "chat_id": 1,

                "title": 1,

                "created_at": 1,

                "updated_at": 1
            }

        ).sort(
            "updated_at",
            -1
        )


        chat_list = list(chats)


        return jsonify(chat_list)


    except Exception as e:

        print("CHAT HISTORY ERROR:", e)

        return jsonify({

            "error": str(e)

        }), 500


# ==========================================
# Get Messages Of Specific Chat
# ==========================================

@app.route("/chats/<chat_id>", methods=["GET"])
def get_chat_messages(chat_id):

    try:

        # Check whether chat exists
        chat = chats_collection.find_one(

            {
                "chat_id": chat_id
            },

            {
                "_id": 0
            }

        )


        if not chat:

            return jsonify({

                "error": "Chat not found"

            }), 404


        # Get messages
        messages = messages_collection.find(

            {
                "chat_id": chat_id
            },

            {
                "_id": 0,

                "role": 1,

                "content": 1,

                "created_at": 1
            }

        ).sort(

            "created_at",
            1

        )


        message_list = list(messages)


        return jsonify({

            "chat_id": chat_id,

            "title": chat.get(
                "title",
                "New Conversation"
            ),

            "messages": message_list

        })


    except Exception as e:

        print("GET CHAT ERROR:", e)

        return jsonify({

            "error": str(e)

        }), 500


# ==========================================
# Run Flask Server
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
