import random
import time

import streamlit as st
import numpy as np
from openai import OpenAI

def hello_app():
    with st.chat_message("user"):
        st.write("Hello 👋")

def hello_app_barchar1():
    
    with st.chat_message("assistant"):
        st.write("Hello human. Showing a simple bar chart from randomly generated data")
        chart_data = np.random.randn(30, 3)
        print('chart_data: \n', chart_data)
        st.bar_chart(chart_data) # create a bar chart with simple instructions. 3 columns and 30 rows

def hello_app_barchart2():
    message = st.chat_message("assistant")
    txt = "Hello human. Showing a simple bar chart from randomly generated data"
    chart_data = np.random.randn(30, 3)
    print('chart_data: \n', chart_data)

    message.write(txt)
    message.bar_chart(chart_data)


# st.chat_input
# st.chat_input lets you display a chat input widget so the user can type in a message.

def hello_user_chat_echo():
    print('method hello_user_chat_echo() called ...')
    # message = st.chat_message("assistant")
    prompt = st.chat_input("Say something")
    if prompt:
        print('showing prompt input by user:  ...', prompt)
        st.write(f"User has sent the following prompt: {prompt}")

    print('method hello_user_chat_echo() DONE ...')


def get_user_input(): # Upon a new user input, add user message to chat history
    # React to user input
    prompt = st.chat_input("Say something")
    role="user"

    if prompt:
        # Display user message in chat message container
        new_chat_msg(role=role, msg=prompt)

        # with st.chat_message("user"):
        #     st.markdown(prompt)
        # # Add user message to chat history
        # add_msg_history("user", prompt)
    return prompt

def add_msg_history(role, msg):
    print('method add_msg_history() called ...')
    st.session_state.messages.append({"role": role, "content": msg})
    pass

def display_new_chat_msg(role, msg):
    print('method display_new_chat_msg() called ...')
    # Display assistant response in chat message container
    with st.chat_message(role):
        st.markdown(msg)

def new_chat_msg(role, msg, add_to_hist=True):
    print('method new_chat_msg() called ...')

    # Display assistant response in chat message container
    display_new_chat_msg(role, msg)

    # Add msg to chat history
    if add_to_hist:
        add_msg_history(role, msg)

    pass

def hello_user_echobot2():
    print('method hello_user_echobot2() called ...')

    st.title("Echo Bot")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = get_user_input()

    if prompt:
        response = f"Echo: {prompt}"
        new_chat_msg("assistant", response)


    print('method hello_user_echobot2() DONE ...')

def init_chat_hist():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_initial_chat_hist():
    # Initialize chat history
    init_chat_hist()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        display_new_chat_msg(role=message["role"], msg=message["content"])


def get_chat_response(prompt):
    response = f"Echo: {prompt}"
    return response


def user_input_resp_one_iteration(response_func=get_chat_response):
    # get user from input
    prompt = get_user_input()

    # if valid input create a response from echo bot
    if prompt:
        response = response_func(prompt=prompt)
        new_chat_msg("assistant", response)


def hello_user_echobot3():
    print('method hello_user_echobot3() called ...')

    st.title("Echo Bot")

    # Initialize chat history
    display_initial_chat_hist()
    
    # get user from input
    prompt = get_user_input()

    # if valid input create a response from echo bot
    if prompt:
        response = f"Echo: {prompt}"
        new_chat_msg("assistant", response)

    print('method hello_user_echobot3() DONE ...')



def hello_user_echobot4():
    print('method hello_user_echobot4() called ...')

    st.title("Echo Bot")

    # Initialize chat history
    display_initial_chat_hist() # stored in chat session

    user_input_resp_one_iteration()
    
    print('method hello_user_echobot4() DONE ...')



# Streamed response emulator
def random_response_generator(prompt):
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )

    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def user_input_resp_typewriter_effect(response_func=random_response_generator):
    # get user from input
    prompt = get_user_input()

    # if valid input create a response from echo bot
    if prompt:
        response_words_gen = response_func(prompt=prompt)
        response = st.write_stream(response_words_gen)
        add_msg_history("assistant", response)

#####################
def init_session():
    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

def hello_user_random_bot1():
    print('method hello_user_random_bot1() called ...')

    st.title("Random Memory Bot")

    # Initialize chat history
    display_initial_chat_hist() # stored in chat session

    # user_input_resp_one_iteration(response_func=random_response_generator)
    user_input_resp_typewriter_effect(response_func=random_response_generator)
    
    print('method hello_user_random_bot1() DONE ...')


def create_chat_stream(role, model, llm_client):
    last_messages = get_all_session_messages()
    with st.chat_message(role):
        stream = llm_client.chat.completions.create(
            model=model,
            messages=last_messages,
            stream=True,
        )

        return stream
    
    return None

def create_response_stream(llm_client, role):
    
    model = st.session_state["openai_model"]
    # last_messages = get_all_session_messages()
    response_stream = create_chat_stream(role=role, model=model, llm_client=llm_client)

    return response_stream

def get_llm_response_and_display(llm_client):
    role="assistant"
    response_stream = create_response_stream(llm_client, role=role)
    response = st.write_stream(response_stream) # add response content to the next chat
    add_msg_history(role=role, msg=response)


def get_all_session_messages():
    messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    return messages


def get_llm_client():
    # Set OpenAI API key from Streamlit secrets
    llm_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Set a default model
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"


def get_llm_response():
    # Display assistant response in chat message container
    get_llm_response_and_display(llm_client=None)



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
    hello_user_random_bot1()

    print('method main_app() DONE ...')


main_app()
#################