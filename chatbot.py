import streamlit as st
import time

# Use the TESDA logo URL or local path here (replace with your path or URL)
TESDA_LOGO_URL = "data:image/jpeg;base64,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"

# --------------------------
# Simple rule-based chatbot function (unchanged)
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").lower().strip()
    if user_message in ["hi", "hello", "hey", "start"]:
        return "👋 Hello! How can I help you today?"
    elif "create account" in user_message or user_message == "1":
        return "📝 You can create an account here: https://e-tesda.gov.ph/login/signup.php"
    elif "courses" in user_message or user_message == "2":
        return "📦 Sure! Explore the available courses here: https://e-tesda.gov.ph/course"
    elif "talk to agent" in user_message or user_message == "3":
        return "📞 Okay, I’m connecting you to our human support staff."
    else:
        return "❓ Sorry, I didn’t understand that. Please choose an option below or type 'help'."

# --------------------------
# Page config and session
# --------------------------
st.set_page_config(page_title="TESDA Cagayan PO Chatbot", page_icon=TESDA_LOGO_URL, layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA Cagayan PO Chatbot. Type 'help' to see options.")]

if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Add custom CSS for background and style logo
# --------------------------
st.markdown(
    f"""
    <style>
    /* Background image with some opacity */
    .stApp {{
        background-image: url('{TESDA_LOGO_URL}');
        background-size: 500px;
        background-repeat: no-repeat;
        background-position: center;
        z-index: -1;
    }}
    /* Override the background opacity only on background, not whole content */
    .stApp > .main {{
        background-color: rgba(255, 255, 255, 0.95);
        padding-top: 70px;
    }}
    /* Style the top logo image */
    .top-logo {{
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 70px;
        height: 70px;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Sidebar info + reset unchanged
# --------------------------
with st.sidebar:
    st.markdown("<img src='{TESDA_LOGO_URL}' alt='TESDA Logo' class='top-logo'/>")
    st.title("About this Chatbot")
    st.write("TESDA Cagayan chatbot** built with Streamlit. You can:")
    st.markdown("""
    - 👋 Greet the bot  
    - 📝 Create an account  
    - 📦 View courses  
    - 📞 Talk to a human agent  
    """)
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA Chatbot. Type 'help' to see options.")]
        st.session_state.last_action = None
        st.experimental_rerun()

# --------------------------
# Top title with fixed TESDA logo
# --------------------------
st.markdown(
    f"<h1 style='text-align: center; color: #4CAF50;'>Rule-Based Chatbot</h1>",
    unsafe_allow_html=True,
)
st.write("Interact with the chatbot by typing or using quick action buttons below.")

# --------------------------
# Quick action buttons (safe pattern)
# --------------------------
col1, col2, col3 = st.columns(3)
if col1.button("📝 Create Account"):
    st.session_state.last_action = "create account"
if col2.button("📦 Courses"):
    st.session_state.last_action = "courses"
if col3.button("📞 Talk to Agent"):
    st.session_state.last_action = "talk to agent"

# --------------------------
# Determine user_input:
# - priority: last_action (button) -> chat_input (if available) -> text_input fallback
# --------------------------
user_input = None

# If a button was clicked (last_action set), consume it exactly once
if st.session_state.last_action:
    user_input = st.session_state.last_action
    # clear it immediately so it won't repeat on next run
    st.session_state.last_action = None

# Try to use chat_input (Streamlit >= 1.25). If not available, fall back to text_input.
try:
    # chat_input returns a value only when user submits
    if user_input is None:
        chat_in = st.chat_input("Type your message here...")
        if chat_in:
            user_input = chat_in
except Exception:
    # fallback to text_input with a session_state key so we can clear it after processing
    if user_input is None:
        # use a session key so we can reset it safely
        if "typed_value" not in st.session_state:
            st.session_state.typed_value = ""
        typed = st.text_input("Type your message here:", value=st.session_state.typed_value, key="typed_value")
        # Only process if not empty and not same as last processed (to avoid reprocessing)
        if typed and (len(st.session_state.messages) == 0 or st.session_state.messages[-1] != ("You", typed)):
            user_input = typed

# --------------------------
# Process a single user_input (if any)
# --------------------------
if user_input:
    # Append user message
    st.session_state.messages.append(("You", user_input))

    # Simulate typing effect (non-blocking visual)
    with st.spinner("Bot is typing..."):
        time.sleep(0.9)

    # Get bot reply
    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ An internal error occurred while generating a reply: {e}"

    st.session_state.messages.append(("Bot", bot_reply))

    # If using the text_input fallback, clear stored value after processing
    if "typed_value" in st.session_state:
        st.session_state.typed_value = ""

# --------------------------
# Display conversation safely
# --------------------------
for entry in st.session_state.messages:
    # defensive check to avoid unpacking errors
    if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
        # skip malformed entries
        continue
    role, msg = entry
    if role == "You":
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:15px; margin:5px; text-align:right;'>"
            f"🧑 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color:#E6E6FA; padding:10px; border-radius:15px; margin:5px; text-align:left;'>"
            f"🤖 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
