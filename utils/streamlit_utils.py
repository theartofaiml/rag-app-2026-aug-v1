import streamlit as st
from google import genai
import os


# client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
# res = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="Say hello to an Agile Coach building an AI assistant!"
# )
# print(res.text)


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


def get_all_session_messages():
    messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]
    return messages


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


def init_session(title):
    st.title(title)
    display_initial_chat_hist()


####################
def get_user_input(): # Upon a new user input, add user message to chat history
    # React to user input
    prompt = st.chat_input("Say something")
    role="user"

    if prompt:
        # Display user message in chat message container
        new_chat_msg(role=role, msg=prompt)
    return prompt

def user_input_resp_one_iteration(response_func):
    # get user from input
    prompt = get_user_input()

    # if valid input create a response from echo bot
    if prompt:
        print('user_input_resp_one_iteration(): Got prompt = ', prompt)
        last_messages = get_all_session_messages()
        prompt2 = "\n".join([ x["content"] for x in last_messages])
        print('user_input_resp_one_iteration(): Sending prompt with context = ', prompt2)
        prompt3 = prompt2 + "\n\n" + "the next questions is: \n" + prompt

        response = response_func(prompt=prompt3)

        print('user_input_resp_one_iteration(): Got response = ', response)
        new_chat_msg("assistant", response)
        return response


def fetch_response_stream_and_display(response_stream, role="assistant"):
    response = st.write_stream(response_stream) # add response content to the next chat
    add_msg_history(role=role, msg=response)
    return response



# def user_input_resp_typewriter_effect(response_func):
#     # get user from input
#     prompt = get_user_input()

#     # if valid input create a response from echo bot
#     if prompt:
#         response_words_gen = response_func(prompt=prompt)
#         response = st.write_stream(response_words_gen)
#         add_msg_history("assistant", response)
#         return response

####### LLM ###################

GEMINI_API_KEY="GEMINI_API_KEY"
OPENAI_API_KEY="OPENAI_API_KEY"
# DEFAULT_CHAT_MODEL_GEMINI="gemini-2.5-flash"
DEFAULT_CHAT_MODEL_GEMINI="gemini-3.6-flash"


def get_gemini_client_response(gemini_client, prompt_contents,  model=DEFAULT_CHAT_MODEL_GEMINI):
    response = gemini_client.models.generate_content(
        model=model,
        contents=prompt_contents
    )

    response_text = response.text
    print(response_text)
    return response_text


def get_gemini_client(api_secret_key):
    client = genai.Client(api_key=api_secret_key)
    return client


def get_secret_(KEY_NAME):
    secret_val=st.secrets[KEY_NAME]
    return secret_val
