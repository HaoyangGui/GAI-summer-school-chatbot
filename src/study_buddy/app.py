from pathlib import Path
import html
import time

import streamlit as st

from study_buddy.chatbot import build_bot


APP_TITLE = "Study Buddy Chatbot"


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="centered",
)


CUSTOM_CSS = """
<style>
    .block-container {
    max-width: 900px;
    padding-top: 3.5rem;
    padding-bottom: 6rem;
}

.top-bar {
    display: flex;
    align-items: center;
    gap: 0.9rem;
    width: 100%;
    box-sizing: border-box;
    padding: 1.15rem 1.35rem;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.10);
    margin: 0 0 1.5rem 0;
    overflow: visible;
}

    .bot-avatar-large {
        width: 54px;
        height: 54px;
        border-radius: 50%;
        background: linear-gradient(135deg, #93c5fd, #a78bfa);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
        position: relative;
        flex-shrink: 0;
    }

    .online-dot {
        position: absolute;
        right: 1px;
        bottom: 2px;
        width: 14px;
        height: 14px;
        background: #22c55e;
        border: 2px solid #0e1117;
        border-radius: 50%;
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.8);
    }

    .top-title {
        font-size: 1.45rem;
        font-weight: 800;
        margin: 0;
    }

    .top-subtitle {
        color: #aeb7c8;
        font-size: 0.92rem;
        margin-top: 0.15rem;
    }

    .chat-list {
        margin-top: 1.2rem;
    }

    .message-row {
        display: flex;
        gap: 0.65rem;
        margin: 0.9rem 0;
        align-items: flex-end;
    }

    .message-row.user {
        justify-content: flex-end;
    }

    .message-row.assistant {
        justify-content: flex-start;
    }

    .avatar-small {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: linear-gradient(135deg, #93c5fd, #a78bfa);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
        position: relative;
    }

    .avatar-small.talking {
        animation: avatarPulse 0.8s infinite ease-in-out;
    }

    .mini-mouth {
        position: absolute;
        bottom: 8px;
        left: 13px;
        width: 8px;
        height: 3px;
        border-radius: 10px;
        background: #111827;
        opacity: 0.75;
    }

    .avatar-small.talking .mini-mouth {
        animation: mouthTalk 0.35s infinite ease-in-out;
    }

    @keyframes avatarPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.06); }
    }

    @keyframes mouthTalk {
        0%, 100% { height: 3px; }
        50% { height: 8px; }
    }

    .bubble {
        max-width: 72%;
        padding: 0.85rem 1rem;
        border-radius: 20px;
        line-height: 1.55;
        font-size: 0.98rem;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    .bubble.user {
        background: #7c3aed;
        color: white;
        border-bottom-right-radius: 6px;
    }

    .bubble.assistant {
        background: rgba(255, 255, 255, 0.08);
        color: #f5f7fb;
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-bottom-left-radius: 6px;
    }

    .typing-bubble {
        display: flex;
        gap: 0.25rem;
        align-items: center;
        width: fit-content;
    }

    .typing-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #cbd5e1;
        animation: typingBounce 1s infinite ease-in-out;
    }

    .typing-dot:nth-child(2) {
        animation-delay: 0.15s;
    }

    .typing-dot:nth-child(3) {
        animation-delay: 0.3s;
    }

    @keyframes typingBounce {
        0%, 80%, 100% { transform: translateY(0); opacity: 0.45; }
        40% { transform: translateY(-5px); opacity: 1; }
    }

    .suggestion-title {
        color: #aeb7c8;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .stButton > button {
        border-radius: 999px;
    }
</style>
"""


def get_bot():
    return build_bot(
        config_path=Path("config/study_buddy.toml"),
        state_path=Path(".study_buddy_state.json"),
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="top-bar">
            <div class="bot-avatar-large">
                🤖
                <span class="online-dot"></span>
            </div>
            <div>
                <div class="top-title">Study Buddy Chatbot</div>
                <div class="top-subtitle">Online · Ready to help you study</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_message(role: str, content: str) -> None:
    safe_content = html.escape(content)

    if role == "user":
        st.markdown(
            f"""
            <div class="message-row user">
                <div class="bubble user">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="message-row assistant">
                <div class="avatar-small">
                    🤖
                    <span class="mini-mouth"></span>
                </div>
                <div class="bubble assistant">{safe_content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_typing_indicator() -> None:
    st.markdown(
        """
        <div class="message-row assistant">
            <div class="avatar-small talking">
                🤖
                <span class="mini-mouth"></span>
            </div>
            <div class="bubble assistant typing-bubble">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot" not in st.session_state:
    st.session_state.bot = get_bot()

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


with st.sidebar:
    st.header("About")
    st.write(
        "Study Buddy helps students understand concepts, plan revision, "
        "make flashcards, and prepare for exams. It refuses off-topic "
        "or homework-cheating requests politely."
    )

    if st.button("Reset conversation", use_container_width=True):
        st.session_state.bot.chat("/reset")
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.success("Conversation reset.")


render_header()


if not st.session_state.messages:
    st.markdown('<div class="suggestion-title">Try one of these:</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Explain derivatives", use_container_width=True):
            st.session_state.pending_prompt = (
                "I am studying calculus. Can you explain derivatives simply?"
            )
            st.rerun()

    with col2:
        if st.button("Make flashcards", use_container_width=True):
            st.session_state.pending_prompt = (
                "Can you make me 5 flashcards about photosynthesis?"
            )
            st.rerun()

    with col3:
        if st.button("Create study plan", use_container_width=True):
            st.session_state.pending_prompt = (
                "I have a biology exam in 4 days on cells, DNA, and evolution. "
                "Can you make me a study plan?"
            )
            st.rerun()


st.markdown('<div class="chat-list">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

if st.session_state.pending_prompt:
    prompt_to_send = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

    st.session_state.messages.append({"role": "user", "content": prompt_to_send})
    render_message("user", prompt_to_send)

    typing_placeholder = st.empty()
    with typing_placeholder:
        render_typing_indicator()

    time.sleep(0.4)
    response = st.session_state.bot.chat(prompt_to_send)

    typing_placeholder.empty()
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)


prompt = st.chat_input("Message Study Buddy...")

if prompt:
    st.session_state.pending_prompt = prompt
    st.rerun()