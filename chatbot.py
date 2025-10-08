import streamlit as st
import time

# Use the TESDA logo URL or local path here (replace with your path or URL)
TESDA_LOGO_URL = "logo.png"

# --------------------------
# Simple rule-based chatbot function (unchanged)
# --------------------------

def reset_chat():
    st.session_state.messages = [("Bot", "👋 Hi! Welcome to TESDA Chatbot. Type 'help' to see options.")]
    st.session_state.last_action = None
    
def chatbot_response(user_message: str) -> str:
    user_message = (user_message or "").lower().strip()
    
    if user_message in ["hi", "hello", "hey", "start"]:
        return "👋 Hello! How can I help you today?"
    
    elif "create account" in user_message or user_message in ["1", "4", "5", "6", "7", "8"]:
        return ('👨‍🎓 <a href="https://e-tesda.gov.ph/login/signup.php" target="_blank">'
                '<b>Create an Account</b></a> 🔗')

    elif "courses" in user_message or user_message == "2":
        return ('📝 <a href="https://e-tesda.gov.ph/course" target="_blank">'
                '<b>View Available Courses</b></a> 📚')

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
    st.title("About this Chatbot")
    st.write("TESDA Cagayan chatbot built with Streamlit. You can:")
    st.markdown("""
    - 👋 Greet the bot
    - 👨‍🎓 Create an account  
    - 📝 View courses  
    - 📞 Talk to a human agent  
    """)

# --------------------------
# Top title with fixed TESDA logo
# --------------------------
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="{TESDA_LOGO_URL}" alt="TESDA Logo" style="width: 120px; height: auto; margin-bottom: 10px;" />
        <h1 style="color: #1E90FF; margin-top: 0;">TESDA Cagayan Chatbot</h1>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("Interact with the chatbot by typing or using quick action buttons below.")

# --------------------------
# Quick action buttons (safe pattern)
# --------------------------
col1, col2, col3, col4 = st.columns(4)
if col1.button("👨‍🎓 Create Account"):
    st.session_state.last_action = "create account"
if col2.button("📝 Courses"):
    st.session_state.last_action = "courses"
if col3.button("📞 Talk to Agent"):
    st.session_state.last_action = "talk to agent"
if col4.button("🔄 Reset Chat", on_click=reset_chat):
    pass

# --------------------------
# Determine user_input:
# - priority: last_action (button) -> chat_input (if available) -> text_input fallback
# --------------------------
user_input = None

# If a button was clicked (last_action set), consume it exactly once
# Always show the chat input
chat_in = None
try:
    chat_in = st.chat_input("Type your message here...")
except Exception:
    pass

# Prioritize button click (last_action), then chat input
if st.session_state.last_action:
    user_input = st.session_state.last_action
    st.session_state.last_action = None
elif chat_in:
    user_input = chat_in
    
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
            f"""<div style='background-color:#E6E6FA; padding:10px; border-radius:15px; margin:5px; text-align:left;'>
            🤖 <b>{role}:</b> {msg}
            </div>""",
            unsafe_allow_html=True,
        )
