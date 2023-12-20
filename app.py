# Principal
import streamlit as st

# st components
from st_components.st_init import set_style
from st_components.st_main import st_main
from st_components.st_session_states import init_session_states
from st_components.st_sidebar import st_sidebar

# validation

set_style()

st.title("💬 Open Code Interpreter")

init_session_states()

st_sidebar()

st_main()
