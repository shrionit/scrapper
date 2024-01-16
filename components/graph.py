from tools import get_token_count
import streamlit


def generateGraph(st: streamlit, data: [str]):
    token_counts = [get_token_count(text) for text in data]
    st.bar_chart(token_counts)
