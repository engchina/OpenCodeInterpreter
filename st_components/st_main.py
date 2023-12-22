import uuid

import streamlit as st

# Database
from st_components.data.database import get_chats_by_conversation_id, save_conversation
from st_components.data.models import Conversation
from st_components.st_conversations import init_conversations
from st_components.st_messages import chat_with_interpreter


def st_main():
    # try:
    if not st.session_state['chat_ready']:

        introduction()

    else:

        create_or_get_current_conversation()

        render_messages()

        chat_with_interpreter()


# except Exception as e:
#     st.error(e)

def create_or_get_current_conversation():
    if 'current_conversation' not in st.session_state:
        conversations, conversation_options = init_conversations()
        if conversations:
            st.session_state['current_conversation'] = conversations[0]
        else:
            conversation_id = str(uuid.uuid4())
            new_conversation = Conversation(conversation_id, st.session_state.user_id,
                                            f"Conversation {len(conversations)}")
            save_conversation(new_conversation)
            st.session_state['current_conversation'] = new_conversation
            st.session_state["messages"] = []
            st.rerun()
    else:
        st.session_state.messages = get_chats_by_conversation_id(st.session_state['current_conversation']["id"])


def render_messages():
    # RENDER MESSAGES
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message(msg["role"]).markdown(f'<p>{msg["content"]}</p>', True)
        elif msg["role"] == "assistant":
            st.chat_message(msg["role"]).markdown(msg["content"])


def introduction():
    # Introduction
    st.info("👋 ようこそ！👋 ")
