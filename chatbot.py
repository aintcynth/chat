import streamlit as st
import time

# Use the TESDA logo URL or local path here (replace with your path or URL)
TESDA_LOGO_URL = "https://user-gen-media-assets.s3.amazonaws.com/seedream_images/8fcf2e33-ebcc-4027-bf34-b983a6dccc0d.png"

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
        background-size: 150px 150px;
        background-repeat: no-repeat;
        background-position: center top;
        background-attachment: fixed;
        opacity: 0.1;
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
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------
# Sidebar info + reset unchanged
# --------------------------
with st.sidebar:
    st.title("ℹ️ About this Chatbot")
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
    f"<img src='{TESDA_LOGO_URL}' alt='TESDA Logo' class='top-logo'/><h1 style='text-align: center; color: #4CAF50;'>Rule-Based Chatbot</h1>",
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
