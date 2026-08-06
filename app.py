import streamlit as st
from rag import ask

st.title("Company Knowledge Assistant")

question = st.chat_input("Ask a question")

if question:
    answer = ask(question)
    st.write(answer)



def append_expander(st, context):
    with st.expander("Retrieved Context"):
        st.write(context)

def append_sources(st, sources):
    with st.expander("Sources"):
        for source in sources:
            st.write(source)
