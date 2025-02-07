from dotenv import load_dotenv
import os
import google.generativeai as genai
from warnings import filterwarnings
import streamlit as st

# Ignore warnings
filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Fetch API key
api_key = os.getenv("google_api_akey")

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Chatbot function with error handling
def chatbot_response(user_prompt):
    response = model.generate_content(user_prompt)

    # Check if response is valid
    if response.candidates and response.candidates[0].finish_reason != 4:
        return response.text  # ✅ Return valid response
    else:
        return "⚠️ Sorry, I can't generate a response due to content restrictions."

# Streamlit Interface
st.set_page_config(page_title="NeuraSeek", page_icon="🤖", layout="centered")

st.title("✨NeuraSeek - Your Assistant✨")
st.write("Powered by Google Generative AI")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state["history"] = []

# Display chat history with new layout
for user_message, bot_message in st.session_state.history:
    # User message on the right
    st.markdown(f"""
    <div style="
        background-color: #d1d3e0;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 70%;
        text-align: right;
        display: inline-block;
        float: right;
    ">
        <p style="margin: 0; font-size: 16px; line-height: 1.5;"><b>You:</b> {user_message} 😊</p>
    </div>
    """, unsafe_allow_html=True)

    # Bot message on the left
    st.markdown(f"""
    <div style="
        background-color: #e1ffc7;
        border-radius: 15px;
        padding: 10px 15px;
        margin: 5px 0;
        max-width: 100%;
        text-align: left;
        display: inline-block;
        float: left;
    ">
        <p style="margin: 0; font-size: 16px; line-height: 1.5;"><b>Neuron:</b> {bot_message} 🤖</p>
    </div>
    """, unsafe_allow_html=True)

    # Reset float after each pair of messages
    st.markdown("<div style='clear: both;'></div>", unsafe_allow_html=True)

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your query here:", max_chars=2000)
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input:
            response = chatbot_response(user_input)
            st.write(f"**Neuron:** {response}")  # ✅ Display response immediately
            st.session_state.history.append((user_input, response))  # ✅ Save history
        else:
            st.warning("Please enter a query.")

# Footer
st.write("\n\n\n\n\n\n\n\n")
st.write("Copy© 2025 Adeel Munir | Made With ❤️ in Pakistan")
