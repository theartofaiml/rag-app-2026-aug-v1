import random
import time

import streamlit as st
import numpy as np
from openai import OpenAI
import utils.streamlit_utils as stutl 
import gradio_client
# from gradio_client import Client


DEFAULT_CHAT_MODEL="gpt-3.5-turbo"

# def get_llm_response_and_display(llm_client, role="assistant", prompt=""):
#     response_stream = create_chat_stream(llm_client=llm_client, role=role, prompt=prompt)
    
#     response = st.write_stream(response_stream) # add response content to the next chat
#     stutl.add_msg_history(role=role, msg=response)
#     return response


def create_chat_stream(llm_client, role="assistant", model=None, prompt=""):
    if model is None:
        model = st.session_state["openai_model"]

    last_messages = stutl.get_all_session_messages()
    with st.chat_message(role):
        stream = llm_client.chat.completions.create(
            model=model,
            messages=last_messages,
            stream=True,
        )

        return stream
    
    return None

def get_llm_client():
    # Set OpenAI API key from Streamlit secrets
    llm_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = DEFAULT_CHAT_MODEL

    return llm_client


def get_llm_client_gemini():

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = stutl.DEFAULT_CHAT_MODEL_GEMINI

    # Set OpenAI API key from Streamlit secrets
    api_key=stutl.get_secret_(stutl.GEMINI_API_KEY)
    llm_client_gemini = stutl.get_gemini_client(api_secret_key=api_key)

    return llm_client_gemini

def get_llm_chatgpt1_response(prompt, role="assistant"):
    llm_client = get_llm_client()
    response_stream = create_chat_stream(llm_client=llm_client, role=role, prompt=prompt)
    response = stutl.fetch_response_stream_and_display(response_stream=response_stream, role=role)
    print(response)


def get_llm_gemini_response(prompt, role="assistant"):
    llm_client = get_llm_client_gemini()
    response = stutl.get_gemini_client_response(gemini_client=llm_client, prompt_contents=prompt)
    print('get_llm_gemini_response() ======= > \n',response)
    return response

def get_temp_llm_response(prompt):
    print('get_temp_llm_response(). called with prompt: ', prompt)

    temp_llm_url=stutl.get_secret_("TEMP_LLM_URL")
    print('get_temp_llm_response(). temp_llm_url=', temp_llm_url)

    # client = Client("http://127.0.0.1:7862")
    print('get_temp_llm_response(). temp_llm_url=', temp_llm_url)

    llm_client = gradio_client.Client(temp_llm_url)
    result = llm_client.predict(
        message=prompt,
        api_name="/chat",
    )

    print(result)
    return result


def llm_chatgpt1_main():
    # Display assistant response in chat message container
    stutl.init_session(title="Toy ChatGPT")

    # take input from user and then call response_func to get response
    # display response to the chat
    # resp_func=get_llm_gemini_response
    resp_func=get_temp_llm_response
    response = stutl.user_input_resp_one_iteration(response_func=resp_func)


############################
def main_app():
    print('method main_app() called ...')
    # hello_app()
    # hello_app2()
    # hello_app_barchart2()
    # hello_user_chat_echo()
    # hello_user_echobot2()
    # hello_user_echobot3()
    # hello_user_echobot4()
    llm_chatgpt1_main()

    print('method main_app() DONE ...')


main_app()
#################