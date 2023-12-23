import os

import streamlit as st
from streamlit.components.v1 import html
from streamlit_extras.add_vertical_space import add_vertical_space

from st_components.st_conversations import conversation_navigation


def st_sidebar():
    # try:
    with st.sidebar:
        # Select choice of API Server
        api_server = st.radio('API の設定', ['Local LLM'], horizontal=True)

        # Set credentials based on choice of API Server
        if api_server == 'Local LLM':
            set_local_llm_server_credentials()

        # Section dedicated to navigate conversations
        conversation_navigation()

        # Section dedicated to About Us
        # about_us()


# except Exception as e:
#     st.error(e)

def about_us():
    add_vertical_space(8)
    html_chat = '<center><h5>🤗 Support the project with a donation for the development of new Features 🤗</h5>'
    st.markdown(html_chat, unsafe_allow_html=True)
    button = '<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="blazzmocompany" data-color="#FFDD00" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>'
    html(button, height=70, width=220)
    iframe = '<style>iframe[width="220"]{position: absolute; top: 50%;left: 50%;transform: translate(-50%, -50%);margin:26px 0}</style>'
    st.markdown(iframe, unsafe_allow_html=True)
    add_vertical_space(2)
    st.write('<center><h6>Made with ❤️ by <a href="mailto:blazzmo.company@gmail.com">BlazzByte</a></h6>',
             unsafe_allow_html=True)
    st.write('<center><h6>Contribution 🤝 by <a href="mailto:tranhoangnguyen03@gmail.com">Sergeant113</a></h6>',
             unsafe_allow_html=True)


def set_local_llm_server_credentials():
    with st.expander(label="Settings", expanded=(not st.session_state['chat_ready'])):
        openai_api_base = st.text_input('API Base:', type="default", value="http://192.168.31.15:8000/v1")
        openai_api_key = st.text_input('API Key:', type="password", value="fake_key")
        os.environ['OPENAI_API_BASE'] = openai_api_base
        os.environ['OPENAI_API_KEY'] = openai_api_key
        model = st.selectbox(
            label='🔌 models',
            options=list(st.session_state['models']['openai'].keys()),
            index=2,
            # disabled= not st.session_state.openai_api_key # Comment: Why?
        )
        context_window = st.session_state['models']['openai'][model]['context_window']

        temperature = st.slider('🌡 Temperature', min_value=0.01, max_value=1.0,
                                value=st.session_state.get('temperature', 0.00), step=0.01)
        max_tokens = st.slider('📝 Max tokens', min_value=1, max_value=2048,
                               value=st.session_state.get('max_tokens', 2048), step=1)

        num_pair_messages_recall = st.slider('**Memory Size**: user-assistant message pairs', min_value=1, max_value=10,
                                             value=2)

        button_container = st.empty()
        save_button = button_container.button("保存 🚀", key='open_ai_save_model_configs')

        if save_button and openai_api_key:
            os.environ['OPENAI_API_BASE'] = openai_api_base
            os.environ["OPENAI_API_KEY"] = openai_api_key
            st.session_state['api_choice'] = 'Local LLM'
            st.session_state['openai_api_base'] = openai_api_base
            st.session_state['openai_api_key'] = openai_api_key
            st.session_state['model'] = model
            st.session_state['temperature'] = temperature
            st.session_state['max_tokens'] = max_tokens
            st.session_state['context_window'] = context_window

            st.session_state['num_pair_messages_recall'] = num_pair_messages_recall

            st.session_state['chat_ready'] = True
            button_container.empty()
            st.rerun()
